from fastapi import FastAPI
from datetime import datetime
from abc import ABC, abstractmethod
import uvicorn
from dotenv import load_dotenv

load_dotenv()

class BaseServer(ABC):
    def __init__(self, title: str, description: str, version: str):
        self.app = FastAPI(title=title, description=description, version=version)
        self.setup_routes()
        self.setup_health_check()

    @abstractmethod
    def setup_routes(self):
        """Abstract method to setup routes. Must be implemented by subclasses."""
        pass

    def setup_health_check(self):
        """Setup a health check route."""
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "server_type": self.app.title.lower().replace(" ", "_"),
            }

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the server."""
        uvicorn.run(self.app, host=host, port=port)