import os
from crypto_com_ai_agent_client import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

cryptocom_agent_sdk_client = create_client(
    {
        "openAI": {"apiKey": os.environ.get("OPENAI_API_KEY"), "model": "gpt-4o"},
        "chainId": 388,
        "customRPC": "https://mainnet.zkevm.cronos.org/",
        "explorerKeys": {
            "cronosZkEvmKey": os.environ.get("CRONOS_ZKEVM_API_KEY"),
        },
    }
)


def test_generate_query(input_query):
    agent_response = cryptocom_agent_sdk_client.agent.generate_query(input_query)
    print(agent_response)


def test_latest_block():
    test_generate_query("get the latest block")


def test_get_balance(address):
    test_generate_query("get the balance of " + address)


if __name__ == "__main__":
    # test_latest_block()
    test_get_balance("0xcf066b771e77391e5cf9cc6fe69ceaced15d863d")
