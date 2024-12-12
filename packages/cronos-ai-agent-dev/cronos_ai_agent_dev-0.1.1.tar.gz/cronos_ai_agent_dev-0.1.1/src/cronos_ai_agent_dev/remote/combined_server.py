from .function_server import FunctionServer
from .route_server import RouteServer

class CombinedServer(RouteServer, FunctionServer):
    def __init__(self, title: str, description: str, version: str, supported_functions: set):
        super().__init__(title, description, version, supported_functions)
        self.setup_routes()