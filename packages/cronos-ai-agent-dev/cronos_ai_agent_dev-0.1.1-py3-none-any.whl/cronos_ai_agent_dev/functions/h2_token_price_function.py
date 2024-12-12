import requests
from .base_function import BaseFunction
...
class H2TokenPriceFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "h2_token_price_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get the price of a token on H2 Finance by its contract address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "token_address": {
                            "type": "string",
                            "description": "The contract address of the token",
                        }
                    },
                    "required": ["token_address"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            token_address = function_arg.get("token_address", "")
            response = requests.get(
                f"https://api.h2.finance/general/api/v1/token/{token_address}/price"
            )
            token_data = response.json()

            if "data" in token_data:
                formatted_response = (
                    f"{token_data['data']['name']} ({token_data['data']['symbol']})\n"
                )
                formatted_response += f"Price: ${token_data['data']['priceUSD']}"
            else:
                formatted_response = "Token price not found"

            return {"success": True, "response": formatted_response}
        except Exception as e:
            return {"success": False, "response": f"Error fetching token price: {e}"}
...
# Register the function
function = H2TokenPriceFunction.register()