from fastapi import FastAPI
from datetime import datetime
from src.tools import Tools
import uvicorn

class BaseServer:
    def __init__(self, title: str, description: str, version: str, supported_functions: set):
        self.app = FastAPI(title=title, description=description, version=version)
        self.tools = Tools()
        self.supported_functions = supported_functions
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/")
        async def health_check():
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "server_type": self.app.title.lower().replace(" ", "_"),
            }

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the FastAPI server using Uvicorn."""
        uvicorn.run(self.app, host=host, port=port)