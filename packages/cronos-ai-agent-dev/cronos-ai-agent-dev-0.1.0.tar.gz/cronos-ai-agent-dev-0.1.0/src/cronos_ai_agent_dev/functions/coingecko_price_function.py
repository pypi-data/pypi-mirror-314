import requests
from .base_function import BaseFunction


class CoingeckoPriceFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "coingecko_price_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get the price of a cryptocurrency in USD.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "coin_id": {
                            "type": "string",
                            "description": "The ID of the cryptocurrency to get the price for.",
                        }
                    },
                    "required": ["coin_id"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            coin_id = function_arg.get("coin_id", "")
            api_response = requests.request(
                method="GET",
                url="https://api.coingecko.com/api/v3/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd"},
            )
            api_result = api_response.json()
            price_usd = api_result.get(coin_id, {}).get("usd", "")
            return {
                "success": True,
                "response": price_usd,
            }
        except Exception as e:
            return {"success": False, "response": f"Error: {e}"}
...
# Register the function
function = CoingeckoPriceFunction.register()