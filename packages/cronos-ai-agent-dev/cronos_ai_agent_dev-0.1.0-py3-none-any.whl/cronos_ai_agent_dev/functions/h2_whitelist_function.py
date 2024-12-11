import requests
from .base_function import BaseFunction


class H2WhitelistFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "h2_whitelist_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get a list of whitelisted tokens on Cronos zkEVM from H2 Finance.",
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            response = requests.get("https://api.h2.finance/general/api/v1/whitelist-tokens")
            tokens = response.json()

            formatted_response = "Available tokens on Cronos zkEVM:\n"
            for token in tokens:
                formatted_response += f"- {token['name']} ({token['symbol']})\n"
                formatted_response += f"  Address: {token['address']}\n"
                formatted_response += f"  Decimals: {token['decimal']}\n"
                formatted_response += f"  Explorer: {token['link']}\n\n"

            return {"success": True, "response": formatted_response}
        except Exception as e:
            return {"success": False, "response": f"Error fetching whitelist tokens: {e}"}


# Register the function
function = H2WhitelistFunction.register()
