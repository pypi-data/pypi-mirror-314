from fastapi import HTTPException
from datetime import datetime
import json
from src.remote.base_server import BaseServer
from src.remote.models import ExecuteRequest, ExecuteResponse, FunctionResult
from src.logger import logger

class FunctionServer(BaseServer):
    def setup_routes(self):
        super().setup_routes()

        @self.app.get("/tools")
        async def get_tools():
            logger.info("All tools: %s", self.tools.function_specs)
            return {
                "specs": [
                    spec for spec in self.tools.function_specs if spec["function"]["name"] in self.supported_functions
                ],
                "prompts": "PRICE_QUERY_INSTRUCTIONS",  # Replace with actual prompts if needed
            }

        @self.app.post("/execute", response_model=ExecuteResponse)
        async def execute_functions(request: ExecuteRequest):
            logger.info("=== Server Received Execute Request ===")
            logger.info("Function Calls: %s", json.dumps(request.dict(), indent=2))

            try:
                outputs = []
                for call in request.function_calls:
                    logger.info("Processing call: %s", call)
                    function_name = call.function["name"]
                    function_args = call.function["arguments"]
                    logger.info("Function name: %s", function_name)
                    logger.info("Function arguments: %s", function_args)

                    if call.type == "function" and function_name in self.supported_functions:
                        logger.info("Executing function %s", function_name)
                        result = self.tools.execute_function(
                            function_name,
                            json.loads(function_args),
                            request.context.get("message", ""),
                            request.context.get("history", []),
                        )
                        logger.info("Function result: %s", result)
                        outputs.append(FunctionResult(tool_call_id=call.id, output=json.dumps(result)))
                    else:
                        logger.warning("Unsupported function: %s", function_name)
                        logger.warning("Supported functions: %s", self.supported_functions)

                response = ExecuteResponse(
                    outputs=outputs,
                    metadata={"processed_at": datetime.utcnow().isoformat(), "server_id": self.app.title.lower().replace(" ", "-")},
                )
                logger.info("Returning response: %s", response)
                return response

            except Exception as e:
                logger.error("Error executing functions: %s", str(e), exc_info=True)
                raise HTTPException(status_code=500, detail=f"Function execution failed: {str(e)}")