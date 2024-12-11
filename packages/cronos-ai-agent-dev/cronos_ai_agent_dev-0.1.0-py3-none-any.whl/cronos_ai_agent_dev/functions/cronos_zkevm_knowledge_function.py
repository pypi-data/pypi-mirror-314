from .base_function import BaseFunction
from ..logger import logger

class CronosZkEvmKnowledgeFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "cronos_zkevm_knowledge_function"

    @property
    def spec(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Query the Cronos zkEVM knowledge base to answer user questions about "
                    "the Cronos zkEVM blockchain and its ecosystem."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_question": {
                            "type": "string",
                            "description": "The user question to be answered by the knowledge base.",
                        }
                    },
                    "required": ["user_question"],
                },
            },
        }

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            logger.info("Querying Cronos zkEVM knowledge base")
            history_formatted = self.memory_instance.format_history_for_cohere(history)
            result = self.knowledge_instance.query_cronos_zkevm_knowledge_base(
                message, history_formatted
            )
            logger.info("Cronos zkEVM knowledge base result: %s", result)
            return {
                "success": True,
                "response": result,
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {e}",
            }


# Register the function
function = CronosZkEvmKnowledgeFunction.register()
