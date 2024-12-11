import time
from .base_function import BaseFunction
from .subgraph.vvs_swaps_query import GRAPHQL_URL, build_graphql_query, retrieve_swaps, organize_transactions, compute_paths_and_totals

class RecentSwapsQueryFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "vvs_recent_swaps_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Query recent swaps from the VVS subgraph",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "seconds_ago": {
                            "type": "integer",
                            "description": "The number of seconds ago to start the query from",
                        }
                    },
                    "required": ["seconds_ago"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            seconds_ago = function_arg.get("seconds_ago", 1800)
            timestamp = int(time.time()) - seconds_ago
            query = build_graphql_query(timestamp)
            swaps = retrieve_swaps(GRAPHQL_URL, query)
            transactions = organize_transactions(swaps)
            total_swaps, path_totals, path_details = compute_paths_and_totals(transactions)

            # Format the response
            formatted_response = f"Number of swaps retrieved: {len(swaps)}\n"
            for (from_address, path), total_amount in total_swaps.items():
                formatted_response += f"From: {from_address}, Path: {path}, Total Amount USD: {total_amount}\n"

            # Add path totals to the response
            formatted_response += "\nPath Totals:\n"
            for path, total_amount in path_totals.items():
                formatted_response += f"Path: {path}, Total Amount USD: {total_amount}\n"

            return {"success": True, "response": formatted_response}
        except Exception as e:
            return {"success": False, "response": f"Error fetching recent swaps: {e}"}

# Register the function
function = RecentSwapsQueryFunction.register()