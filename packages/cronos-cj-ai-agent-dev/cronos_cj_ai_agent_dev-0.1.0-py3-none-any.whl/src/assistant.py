import os
import json
from openai import OpenAI

from src.memory import Memory
from src.tools import Tools
from src.knowledge import Knowledge
from src.prompts import get_full_instructions
from src.logger import logger

class Assistant:
    def __init__(self):
        self.memory_instance = Memory()
        self.tools_instance = Tools()
        self.knowledge_instance = Knowledge()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.assistant = self.client.beta.assistants.create(
            name="Cryptocurrency trading assistant",
            instructions=get_full_instructions(),
            model=self.model,
            tools=self.tools_instance.tools,
        )

    async def run_assistant(self, chat_id: int, message: str, history: list):
        try:
            logger.info("Instantiating assistant run")
            history_formatted = self.memory_instance.format_history_for_openai(history)
            thread = self.client.beta.threads.create()
            for history_item in history_formatted:
                self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role=history_item.get("role", "user"),
                    content=history_item.get("content", ""),
                )
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=message,
            )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=self.assistant.id, timeout=60
            )
            keep_going = True
            n_iterations = 0
            assistant_response = None
            while keep_going and n_iterations < 10:
                n_iterations += 1
                if run.status == "completed":
                    messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                    for message in messages.data:
                        if message.role == "assistant":
                            assistant_response = message.content[0].text.value
                            keep_going = False
                            break
                elif run.status == "requires_action":
                    tool_outputs = []
                    if run.required_action.submit_tool_outputs is not None:
                        tools_calls = run.required_action.submit_tool_outputs.tool_calls
                        for call in tools_calls:
                            call_type = call.type
                            if call_type == "function":
                                call_function_name = call.function.name
                                logger.info("Function name: %s", call_function_name)
                                if call_function_name in self.tools_instance.active_tools:
                                    call_function_argument = json.loads(call.function.arguments)
                                    logger.info("Function argument: %s", call_function_argument)
                                    tool_output = self.tools_instance.execute_function(
                                        function_name=call_function_name,
                                        function_arg=call_function_argument,
                                        message=message,
                                        history=history,
                                    )
                                    tool_output_formatted = {
                                        "tool_call_id": call.id,
                                        "output": tool_output,
                                    }
                                    tool_outputs.append(tool_output_formatted)
                    logger.info("Tool outputs: %s", tool_outputs)
                    if len(tool_outputs) > 0:
                        run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=tool_outputs,
                        )
                        logger.info("Tool outputs submitted")
            if assistant_response is None:
                assistant_response = "Error, please try again."
        except Exception as e:
            logger.error("Error running assistant: %s", e)
            assistant_response = "Error, the conversation has been reset."
        if assistant_response == "Error, the conversation has been reset.":
            self.memory_instance.reset_conversation(chat_id)
        logger.info("Returning assistant response: %s", assistant_response)
        return assistant_response
