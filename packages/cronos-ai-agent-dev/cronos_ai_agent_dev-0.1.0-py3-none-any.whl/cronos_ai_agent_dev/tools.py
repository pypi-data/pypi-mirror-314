import json
import os
from crypto_com_ai_agent_client import create_client

# Import registered functions
from .functions.h2_token_price_function import function as h2_price_function
from .functions.cronos_zkevm_knowledge_function import function as cronos_zkevm_knowledge_function
from .functions.crypto_ids_function import function as crypto_ids_function
from .functions.coingecko_price_function import function as crypto_price_function
from .functions.cdc_agent_sdk_function import function as blockchain_data_function
from .functions.h2_whitelist_function import function as h2_whitelist_function
from .functions.native_balance_function import function as native_balance_function
from .functions.erc20_balance_function import function as erc20_balance_function
from .functions.vvs_recent_swaps_function import function as vvs_recent_swaps_function
from .error_handler import ErrorHandler
from .logger import logger

class Tools:
    def __init__(self):
        # Initialize functions
        self.functions = [
            h2_price_function,
            cronos_zkevm_knowledge_function,
            crypto_ids_function,
            crypto_price_function,
            blockchain_data_function,
            h2_whitelist_function,
            native_balance_function,
            erc20_balance_function,
            vvs_recent_swaps_function,
        ]

        # Create registries from functions
        self.function_registry = {f.name: f.execute for f in self.functions}
        self.function_specs = [f.spec for f in self.functions]

    def execute_function(self, function_name: str, function_arg: dict, message: str, history: list):
        """
        Execute a registered function
        Response format is {"success": True, "response": "response_text"} in text format
        """
        logger.info("Executing function: %s, with arguments: %s", function_name, function_arg)

        if function_name not in self.function_registry:
            return json.dumps(
                {
                    "success": False,
                    "response": f"Function {function_name} is not registered",
                }
            )

        try:
            result = self.function_registry[function_name](function_arg, message, history)
            return json.dumps(result)
        except Exception as e:
            return json.dumps(ErrorHandler.handle_function_error(e, function_name))

    @property
    def tools(self):
        """Return list of all registered function specifications"""
        return self.function_specs

    @property
    def active_tools(self):
        """Return list of all registered function names"""
        return list(self.function_registry.keys())
