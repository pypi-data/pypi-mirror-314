from fastapi import HTTPException
from datetime import datetime
import json
from .base_server import BaseServer
from .models import ExecuteRequest, ExecuteResponse, FunctionResult
from ..logger import logger
from ..tools import Tools
from ..local.custom_assistant import CustomAssistant

class FunctionServer(BaseServer):
    def __init__(self,
                 tools_instance=None,
                 assistant_instance=None,
                 title="Function Server",
                 description="A server to execute functions",
                 version="0.1.0"):
        self.tools_instance = tools_instance if tools_instance is not None else Tools()
        self.assistant = assistant_instance if assistant_instance is not None else CustomAssistant()
        self.function_specs = self.tools_instance.function_specs
        self.function_names = set(self.tools_instance.function_names)
        super().__init__(title=title, description=description, version=version)

    def setup_routes(self):
        @self.app.get("/tools")
        async def get_tools():
            logger.info("All tools: %s", self.tools_instance.function_names)
            return {
                "functions": self.function_names,
                "specs": self.function_specs,
                "prompts": self.assistant.prompts,
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

                    if call.type == "function" and function_name in self.function_names:
                        logger.info("Executing function %s", function_name)
                        result = self.tools_instance.execute_function(
                            function_name,
                            json.loads(function_args),
                            request.context.get("message", ""),
                            request.context.get("history", []),
                        )
                        logger.info("Function result: %s", result)
                        outputs.append(FunctionResult(tool_call_id=call.id, output=json.dumps(result)))
                    else:
                        logger.warning("Unsupported function: %s", function_name)
                        logger.warning("Supported functions: %s", self.function_names)

                response = ExecuteResponse(
                    outputs=outputs,
                    metadata={"processed_at": datetime.utcnow().isoformat(), "server_id": self.app.title.lower().replace(" ", "-")},
                )
                logger.info("Returning response: %s", response)
                return response

            except Exception as e:
                logger.error("Error executing functions: %s", str(e), exc_info=True)
                raise HTTPException(status_code=500, detail=f"Function execution failed: {str(e)}")