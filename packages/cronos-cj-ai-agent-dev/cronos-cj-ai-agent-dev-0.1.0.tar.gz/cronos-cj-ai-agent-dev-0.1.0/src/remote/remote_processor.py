from typing import Optional, Dict, List, Tuple, Any
import json
import os
from openai import OpenAI
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from src.logger import logger

from src.remote.models import (
    MessageContext,
    ProcessedMessage,
    ServerInfo,
    FunctionCall,
)
from .exceptions import RemoteProcessingError


class RemoteProcessor:
    def __init__(self, servers: List[ServerInfo], api_key: Optional[str] = None):
        """
        Initialize with multiple servers
        servers: List of ServerInfo objects containing url and capabilities
        """
        self.servers = servers
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY", ""))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.server_capabilities = {}
        self.executor = ThreadPoolExecutor(max_workers=10)

    async def _fetch_server_capabilities(self) -> None:
        """Fetch tools and prompts from all servers"""

        async def fetch_single_server(server: ServerInfo) -> Tuple[str, Dict]:
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    self.executor, lambda: requests.get(f"{server.url.rstrip('/')}/tools")
                )
                response.raise_for_status()
                data = response.json()
                logger.info(f"Fetched capabilities from {server.url}: {data}")
                return server.url, {
                    "specs": data["specs"],
                    "prompts": data["prompts"],
                    "capabilities": server.capabilities,
                }
            except Exception as e:
                logger.error("Failed to fetch capabilities from %s: %s", server.url, str(e))
                return server.url, None

        tasks = [fetch_single_server(server) for server in self.servers]
        results = await asyncio.gather(*tasks)

        self.server_capabilities = {url: data for url, data in results if data is not None}

        logger.info("Fetched server capabilities:", self.server_capabilities)

    def _create_assistant(self, specs: List[Dict], prompts: str) -> Any:
        """Create OpenAI assistant with given specs and prompts"""
        return self.client.beta.assistants.create(
            name="Cryptocurrency trading assistant",
            instructions=prompts,
            model=self.model,
            tools=specs,
        )

    async def _create_run(self, message: str, history: List[Dict]) -> Dict:
        """Create and manage OpenAI run using combined capabilities"""
        try:
            if not self.server_capabilities:
                await self._fetch_server_capabilities()

            all_specs = []
            all_prompts = []
            for server_data in self.server_capabilities.values():
                all_specs.extend(server_data["specs"])
                all_prompts.append(server_data["prompts"])

            assistant = self._create_assistant(all_specs, "\n\n".join(all_prompts))
            thread = self.client.beta.threads.create()

            for item in history:
                self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role=item.get("role", "user"),
                    content=item.get("content", ""),
                )

            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message,
            )

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=assistant.id, timeout=60
            )

            return {
                "thread_id": thread.id,
                "run_id": run.id,
                "status": run.status,
                "required_action": run.required_action if hasattr(run, "required_action") else None,
                "assistant_id": assistant.id,
            }
        except Exception as e:
            logger.error(f"Failed to create run: {str(e)}")
            raise RemoteProcessingError(f"Failed to create run: {str(e)}")

    async def _execute_function_calls(
        self, server_url: str, function_calls: List[FunctionCall], context: MessageContext
    ) -> Dict[str, Any]:
        """Execute function calls on a specific server"""
        try:
            # Debug print all objects
            logger.info("=== Debug Execute Function Calls ===")
            logger.info(f"Server URL: {server_url}")
            logger.info("Function Calls:")
            for call in function_calls:
                logger.info(f"  ID: {call.id}")
                logger.info(f"  Type: {call.type}")
                logger.info(f"  Function: {call.function}")

            # Create serializable metadata without OpenAI objects
            serializable_metadata = {}
            if context.metadata:
                for key, value in context.metadata.items():
                    if key == "run_info":
                        run_info = {
                            "thread_id": value.get("thread_id"),
                            "run_id": value.get("run_id"),
                            "status": value.get("status"),
                            "assistant_id": value.get("assistant_id"),
                        }
                        serializable_metadata["run_info"] = run_info
                    else:
                        serializable_metadata[key] = value

            # Create request data matching server's ExecuteRequest model
            request_data = {
                "function_calls": [
                    {
                        "id": call.id,
                        "type": call.type,
                        "function": {
                            "name": call.function["name"],
                            "arguments": call.function["arguments"],
                        },
                    }
                    for call in function_calls
                ],
                "context": {
                    "chat_id": context.chat_id,
                    "sender_id": context.sender_id,
                    "message": context.message,
                    "history": context.history or [],
                    "metadata": serializable_metadata,
                },
            }

            logger.info("Sending request data:")
            logger.info(json.dumps(request_data, indent=2))

            response = await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: requests.post(f"{server_url}/execute", json=request_data)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Function execution failed on {server_url}: {str(e)}")
            raise RemoteProcessingError(f"Function execution failed on {server_url}: {str(e)}")

    def _map_functions_to_servers(
        self, function_calls: List[FunctionCall]
    ) -> Dict[str, List[FunctionCall]]:
        """Map function calls to appropriate servers"""
        server_map = {}
        for call in function_calls:
            function_name = call.function["name"]  # Changed from call.function.name
            for server_url, server_data in self.server_capabilities.items():
                server_tools = {tool["function"]["name"] for tool in server_data["specs"]}
                if function_name in server_tools:
                    if server_url not in server_map:
                        server_map[server_url] = []
                    server_map[server_url].append(call)
                    break
        return server_map

    async def process_run_result(
        self, run_result: Dict, context: MessageContext
    ) -> ProcessedMessage:
        """Process OpenAI run result and execute necessary function calls"""
        try:
            keep_going = True
            n_iterations = 0
            assistant_response = None
            thread_id = run_result["thread_id"]
            run_id = run_result["run_id"]

            while keep_going and n_iterations < 10:
                n_iterations += 1
                logger.info(f"Processing iteration {n_iterations}, status: {run_result['status']}")

                if run_result["status"] == "completed":
                    messages = self.client.beta.threads.messages.list(thread_id=thread_id)
                    for message in messages.data:
                        if message.role == "assistant":
                            assistant_response = message.content[0].text.value
                            logger.info(f"Got assistant response: {assistant_response}")
                            keep_going = False
                            break
                    break

                elif run_result["status"] == "requires_action":
                    tool_outputs = []
                    if run_result["required_action"].submit_tool_outputs is not None:
                        tool_calls = run_result["required_action"].submit_tool_outputs.tool_calls

                        function_calls = []
                        for call in tool_calls:
                            if call.type == "function":
                                function_calls.append(
                                    FunctionCall(
                                        id=call.id,
                                        type=call.type,
                                        function={
                                            "name": call.function.name,
                                            "arguments": call.function.arguments,
                                        },
                                    )
                                )
                                logger.info(f"Created function call: {function_calls[-1]}")

                        # Map and execute functions
                        server_map = self._map_functions_to_servers(function_calls)
                        tasks = []
                        for server_url, server_calls in server_map.items():
                            task = self._execute_function_calls(server_url, server_calls, context)
                            tasks.append(task)

                        results = await asyncio.gather(*tasks, return_exceptions=True)

                        # Collect outputs
                        for result in results:
                            if isinstance(result, Exception):
                                logger.error(f"Error executing functions: {str(result)}")
                                continue
                            tool_outputs.extend(result.get("outputs", []))

                        # Submit tool outputs back to OpenAI
                        if tool_outputs:
                            logger.info(f"Submitting {len(tool_outputs)} tool outputs")
                            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                                thread_id=thread_id, run_id=run_id, tool_outputs=tool_outputs
                            )
                            run_result["status"] = run.status
                            run_result["required_action"] = (
                                run.required_action if hasattr(run, "required_action") else None
                            )
                            run_id = run.id
                else:
                    logger.warning(f"Unexpected run status: {run_result['status']}")
                    break

            if assistant_response is None:
                assistant_response = "Error, please try again."

            return ProcessedMessage(
                response=assistant_response,
                updated_history=context.history or [],
                metadata={
                    "run_info": run_result,
                    "iterations": n_iterations,
                    "function_results": tool_outputs if "tool_outputs" in locals() else [],
                },
            )

        except Exception as e:
            logger.error(f"Failed to process run result: {str(e)}", exc_info=True)
            raise RemoteProcessingError(f"Failed to process run result: {str(e)}")

    async def process_message(self, context: MessageContext) -> ProcessedMessage:
        """Process message using OpenAI run and appropriate server"""
        try:
            run_result = await self._create_run(context.message, context.history or [])

            if context.metadata is None:
                context.metadata = {}
            context.metadata["run_info"] = run_result

            return await self.process_run_result(run_result, context)

        except Exception as e:
            raise RemoteProcessingError(f"Message processing failed: {str(e)}")
