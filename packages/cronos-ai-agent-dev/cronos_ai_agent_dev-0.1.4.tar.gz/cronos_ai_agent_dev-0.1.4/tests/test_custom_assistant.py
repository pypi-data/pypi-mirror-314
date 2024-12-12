import sys
import asyncio

from src.cronos_ai_agent_dev.local.custom_assistant import CustomAssistant

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
