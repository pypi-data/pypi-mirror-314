from .base_function import BaseFunction


class CryptoIdsFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "crypto_ids_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get a list of cryptocurrency IDs and their corresponding tickers.",
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        response_text = """The following is a list of cryptocurrency IDs and their corresponding tickers:
bitcoin: BTC
ethereum: ETH
crypto-com-chain: CRO

if didn't get the id, can use the token name directly in the message.
"""
        return {
            "success": True,
            "response": response_text,
        }


# Register the function
function = CryptoIdsFunction.register()