from src.cronos_ai_agent_dev.functions.native_balance_function import NativeBalance
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_native_balance():
    # Initialize the function
    balance_checker = NativeBalance()

    # Test cases with real addresses
    test_addresses = [
        "0x0a2989d3caa2d8955ddbe00bbf52d4ce00bb0b9e",  # Replace with real address
        "0x0000000000000000000000000000000000000000",  # Zero address
        "invalid_address",  # Invalid address test
    ]

    for address in test_addresses:
        print(f"\nTesting address: {address}")
        result = balance_checker.execute({"address": address}, "", [])  # message  # history
        print(f"Success: {result['success']}")
        print(f"Response: {result['response']}")


if __name__ == "__main__":
    test_native_balance()
