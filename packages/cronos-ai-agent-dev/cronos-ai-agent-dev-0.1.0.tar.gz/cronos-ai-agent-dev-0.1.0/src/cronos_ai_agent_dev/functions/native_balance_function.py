from web3 import Web3
from .base_function import BaseFunction
import os


class NativeBalanceFunction(BaseFunction):
    def __init__(self):
        super().__init__()
        rpc_url = os.getenv("CRONOS_ZKEVM_RPC_URL")
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    @property
    def name(self) -> str:
        return "native_balance_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get native zkCRO balance from Cronos zkEVM blockchain.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "The wallet address to query (case-insensitive)",
                        }
                    },
                    "required": ["address"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            address = function_arg.get("address")

            # Validate basic address format
            if not Web3.is_address(address):
                return {"success": False, "response": "Invalid wallet address format"}

            try:
                # Convert to checksum address
                checksum_address = Web3.to_checksum_address(address)
            except ValueError:
                return {"success": False, "response": "Invalid address checksum"}

            # Get balance using checksum address
            balance_wei = self.w3.eth.get_balance(checksum_address)
            balance_eth = self.w3.from_wei(balance_wei, "ether")
            response = f"Native CRO Balance for {checksum_address}:\n"
            response += f"{balance_eth} CRO"

            return {"success": True, "response": response}
        except Exception as e:
            return {"success": False, "response": f"Error: {e}"}


# Register the function
function = NativeBalanceFunction.register()
