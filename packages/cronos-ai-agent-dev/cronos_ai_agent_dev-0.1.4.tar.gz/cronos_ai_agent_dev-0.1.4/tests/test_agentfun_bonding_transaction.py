from dotenv import load_dotenv
from src.cronos_ai_agent_dev.functions.bonding_transaction_function import BondingTransaction

# Load environment variables
load_dotenv()


def test_bonding_transaction():
    # Initialize the BondingTransaction class
    bonding_tx = BondingTransaction()

    # Test parameters
    # Using a known transaction hash and contract address on Cronos zkEVM
    test_params = {
        "transaction_hash": "0x264c2e8b2402d3e1a8098170c6270e0be3700e29f4af702a5b41cae482318f97",
        "contract_address": "0x55F04eF64860Bf4F73bc54DF060f98079Aa5d8F3",
    }

    # Execute the function
    result = bonding_tx.execute(test_params, "", [])

    # Print results
    print("Test Result:")
    print("-" * 50)
    if result["success"]:
        print("Success!")
        print(result["response"])
        print("\nDetailed Data:")
        for key, value in result["data"].items():
            print(f"{key}: {value}")
    else:
        print("Failed!")
        print(result["response"])


def test_launch_transaction():
    bonding_tx = BondingTransaction()

    # Use a real launch transaction hash
    test_params = {
        "transaction_hash": "0x318dadc33b17d71e2d42a41d49fed753d9aca3ee5da31595ac482ff6891b5ff9",
        "contract_address": "0x55F04eF64860Bf4F73bc54DF060f98079Aa5d8F3",
    }

    result = bonding_tx.execute(test_params, "", [])
    print("\nLaunch Transaction Test:")
    print("-" * 50)
    if result["success"]:
        print("Success!")
        print(result["response"])
    else:
        print("Failed!")
        print(result["response"])


def test_buy_transaction():
    bonding_tx = BondingTransaction()

    # Use a real launch transaction hash
    test_params = {
        "transaction_hash": "0x9dff11210bad967063780c5a47f29f5aec0e66f828079004c9452877876cad1c",
        "contract_address": "0x55F04eF64860Bf4F73bc54DF060f98079Aa5d8F3",
    }

    result = bonding_tx.execute(test_params, "", [])
    print("\nBuy Transaction Test:")
    print("-" * 50)
    if result["success"]:
        print("Success!")
        print(result["response"])
    else:
        print("Failed!")
        print(result["response"])


if __name__ == "__main__":
    # Run all tests
    print("Running Bonding Transaction Tests\n")
    test_launch_transaction()
    test_buy_transaction()
