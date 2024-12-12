import requests
from typing import Optional, Dict
from datetime import datetime
import os
from .base_function import BaseFunction


class SentioPriceFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "sentio_price_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get the price of a cryptocurrency from Sentio by its identifier.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "coin_identifier": {
                            "type": "string",
                            "description": "The identifier of the coin (e.g., 'ethereum', 'bitcoin').",
                        },
                        "timestamp": {
                            "type": "string",
                            "description": "The specific timestamp to get the price for, in ISO format.",
                            "format": "date-time",
                        },
                    },
                    "required": ["coin_identifier"],
                },
            },
        }
    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            coin_identifier = function_arg.get("coin_identifier", "")
            timestamp_str = function_arg.get("timestamp", None)
            timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None

            api_key = os.environ.get("SENTIO_API_TOKEN")
            base_url = "https://app.sentio.xyz/api/v1"
            headers = {"Authorization": f"Bearer {api_key}" if api_key else None}

            endpoint = f"{base_url}/prices"
            current_timestamp = (timestamp or datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
            params = {"coinId.symbol": coin_identifier, "timestamp": current_timestamp}
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()

            timestamp_str = data.get("timestamp", "")
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                # Fallback to current time if timestamp parsing fails
                timestamp = datetime.utcnow()

            price_data = {
                "price": data.get("price"),
                "timestamp": timestamp,
                "coin_id": data.get("coin_id"),
            }

            return {
                "success": True,
                "response": price_data,
            }
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return {
                    "success": False,
                    "response": f"Price data not found for coin: {coin_identifier}",
                }
            return {
                "success": False,
                "response": f"HTTP error occurred: {e}",
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error fetching price: {e}",
            }
# Register the function
function = SentioPriceFunction.register()