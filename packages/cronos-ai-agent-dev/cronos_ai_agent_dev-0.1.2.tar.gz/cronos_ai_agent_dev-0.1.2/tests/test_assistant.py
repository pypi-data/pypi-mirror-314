import asyncio
from src.cronos_ai_agent_dev.assistant import Assistant
from dotenv import load_dotenv
import sys

load_dotenv()

chat_id = "test_123"

history = [
    {"role": "user", "message": "Hi"},
    {"role": "assistant", "message": "Hello! How can I help you today?"},
]
async def run_test(chat_id, message, history):
    # Initialize
    assistant = Assistant()

    # Run the assistant
    response = await assistant.run_assistant(chat_id=chat_id, message=message, history=history)

    # Basic assertions
    assert isinstance(response, str)
    assert len(response) > 0

async def test_recent_swaps_query():
    message = sys.argv[1] if len(sys.argv) > 1 else "Show me swaps from the last hour."
    await run_test(chat_id, message, history)

async def test_native_balance_query():
    message = sys.argv[1] if len(sys.argv) > 1 else "Show me the balance of 0xcf1e3699b586b1df761cc638fd8ed830144dbda7."


    await run_test(chat_id, message, history)

if __name__ == "__main__":
    asyncio.run(test_native_balance_query())