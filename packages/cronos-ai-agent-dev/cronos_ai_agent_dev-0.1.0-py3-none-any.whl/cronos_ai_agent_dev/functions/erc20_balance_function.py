from web3 import Web3
from .base_function import BaseFunction
import os
from typing import Optional


class ERC20BalanceFunction(BaseFunction):
    def __init__(self):
        super().__init__()
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("CRONOS_ZKEVM_RPC_URL")))
        self.erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function",
            },
        ]

    def _validate_and_checksum_address(
        self, address: str, address_type: str = "wallet"
    ) -> Optional[str]:
        """
        Validate and convert address to checksum format.

        Args:
            address (str): Ethereum address to validate
            address_type (str): Type of address for error messages ("wallet" or "token")

        Returns:
            str: Checksum address

        Raises:
            ValueError: If address is invalid
        """
        try:
            if not self.w3.is_address(address):
                return None
            return self.w3.to_checksum_address(address)
        except Exception:
            return None

    @property
    def name(self) -> str:
        return "erc20_balance_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get ERC20 token balance from Cronos zkEVM blockchain.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "The wallet address to query (case-insensitive)",
                        },
                        "token_address": {
                            "type": "string",
                            "description": "The ERC20 token contract address (case-insensitive)",
                        },
                    },
                    "required": ["address", "token_address"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            wallet_address = function_arg.get("address")
            token_address = function_arg.get("token_address")
            # Validate and convert wallet address
            checksum_wallet = self._validate_and_checksum_address(wallet_address, "wallet")
            if not checksum_wallet:
                return {
                    "success": False,
                    "response": f"Invalid wallet address format: {wallet_address}",
                }

            # Validate and convert token address
            checksum_token = self._validate_and_checksum_address(token_address, "token")
            if not checksum_token:
                return {
                    "success": False,
                    "response": f"Invalid token address format: {token_address}",
                }

            try:
                # Create contract instance with checksum address
                contract = self.w3.eth.contract(address=checksum_token, abi=self.erc20_abi)
                # Get token info and balance using checksum wallet address
                balance = contract.functions.balanceOf(checksum_wallet).call()
                decimals = contract.functions.decimals().call()
                symbol = contract.functions.symbol().call()
                # Format balance with proper decimals
                formatted_balance = balance / (10**decimals)

                response = (
                    f"Token Balance for {checksum_wallet}:\n"
                    f"{formatted_balance} {symbol}\n"
                    f"Token Address: {checksum_token}\n"
                    f"Decimals: {decimals}"
                )

                return {
                    "success": True,
                    "response": response,
                    "data": {
                        "wallet_address": checksum_wallet,
                        "token_address": checksum_token,
                        "balance": str(balance),
                        "formatted_balance": str(formatted_balance),
                        "symbol": symbol,
                        "decimals": decimals,
                    },
                }

            except Exception as contract_error:
                return {
                    "success": False,
                    "response": (
                        f"Error interacting with token contract at {checksum_token}:\n"
                        f"{str(contract_error)}"
                    ),
                }

        except Exception as e:
            return {"success": False, "response": f"Unexpected error: {str(e)}"}


# Register the function
function = ERC20BalanceFunction.register()
