from .function_server import FunctionServer
from .gateway_server import GatewayServer

class CombinedServer(GatewayServer, FunctionServer):
    def __init__(self, title: str, description: str, version: str, supported_functions: set):
        super().__init__(title, description, version, supported_functions)
        self.setup_routes()