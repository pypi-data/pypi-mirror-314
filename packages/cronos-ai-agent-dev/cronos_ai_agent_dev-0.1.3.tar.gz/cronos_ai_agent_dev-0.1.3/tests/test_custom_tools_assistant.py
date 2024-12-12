from src.cronos_ai_agent_dev.local.base_assistant import BaseAssistant
from src.cronos_ai_agent_dev.local.base_tools import BaseTools
from src.cronos_ai_agent_dev.functions.h2_token_price_function import function as h2_price_function
from src.cronos_ai_agent_dev.functions.h2_whitelist_function import function as h2_whitelist_function
import sys
import asyncio

PRICE_QUERY_PROMPT = """
Price Query Instructions:

1. Implementation Path:
  - First use h2_whitelist_function to check if the token exists in H2 Finance
  - If found in the whitelist, use h2_token_price_function with the found address
  - This path is for tokens specifically on Cronos zkEVM through H2 Finance

2. Workflow:
   - FIRST call h2_whitelist_function to check if the token exists in H2 Finance
   - If found in H2 whitelist: Use the H2 Finance price path
   - If not found in H2 whitelist: Just return don't have the price

3. Example Flow:
   User: "What's the price of TOKEN?"
   Assistant:
   - Calls h2_whitelist_function to check H2 Finance first
   - If found in H2: Uses h2_token_price_function
   - If not found in H2: Just return don't have the price

4. Clarifications Needed If:
   - Token name is ambiguous
   - Multiple matching tokens are found
   - Token cannot be found in either system
   - Token symbol format is invalid
"""


class CustomTools(BaseTools):
    @property
    def register_functions(self):
        return [
            h2_price_function,
            h2_whitelist_function,
        ]

class CustomAssistant(BaseAssistant):
    def __init__(self):
        self.tools = CustomTools()
        super().__init__(tools_instance=self.tools)

    @property
    def prompts(self):
        return "\n\n".join(
        [
          PRICE_QUERY_PROMPT,
        ]
    )

chat_id = "test_123"

history = [
    {"role": "user", "message": "Hi"},
    {"role": "assistant", "message": "Hello! How can I help you today?"},
]

async def main():
    message = sys.argv[1] if len(sys.argv) > 1 else "What can you do?"
    assistant = CustomAssistant()
    response = await assistant.run_assistant(chat_id=chat_id, message=message, history=history)
    print(response)

if __name__ == "__main__":
   asyncio.run(main())