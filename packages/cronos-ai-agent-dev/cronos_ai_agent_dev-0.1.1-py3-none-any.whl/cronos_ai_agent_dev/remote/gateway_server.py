from fastapi import HTTPException, Request
from datetime import datetime
from .base_server import BaseServer
from .models import MessageContext, MessageResponseAPI, ServerInfo
from .remote_processor import RemoteProcessor

class GatewayServer(BaseServer):
    def __init__(self, title: str, description: str, version: str, supported_functions: set, function_servers: list):
        super().__init__(title, description, version, supported_functions)
        self.processor = RemoteProcessor(servers=function_servers)
        self.setup_routes()

    def setup_routes(self):
        super().setup_routes()

        @self.app.post("/query", response_model=MessageResponseAPI)
        async def process_query(request: Request):
            """Process a query by coordinating with function servers"""
            try:
                request_data = await request.json()
                context = MessageContext(
                    chat_id=request_data.get("chat_id"),
                    sender_id=request_data.get("sender_id"),
                    message=request_data.get("message"),
                    is_group=request_data.get("is_group", False),
                    bot_name=request_data.get("bot_name", "default_bot"),
                    metadata={
                        "source": "coordinator",
                        "timestamp": datetime.utcnow().isoformat(),
                        **(request_data.get("metadata") or {}),
                    },
                )

                result = await self.processor.process_message(context)

                return MessageResponseAPI(
                    response=result.response,
                    history=result.updated_history,
                    error=result.error,
                    metadata=result.metadata,
                    timestamp=result.timestamp.isoformat(),
                )

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))