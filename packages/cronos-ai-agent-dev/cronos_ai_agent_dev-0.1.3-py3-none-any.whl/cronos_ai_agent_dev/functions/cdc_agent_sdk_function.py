from .base_function import BaseFunction


class CDCAgentSDKFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "cdc_agent_sdk_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Retrieve data from the Cronos zkEVM blockchain.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_question": {
                            "type": "string",
                            "description": "The question asked by the user in natural language.",
                        }
                    },
                    "required": ["user_question"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            user_question = function_arg.get("user_question", "")
            agent_response = self.cryptocom_agent_sdk_client.agent.generate_query(user_question)
            return {
                "success": True,
                "response": agent_response,
            }
        except Exception as e:
            return {"success": False, "response": f"Error: {e}"}


# Register the function
function = CDCAgentSDKFunction.register()
