from dotenv import load_dotenv
from src.cronos_ai_agent_dev.functions.erc20_balance_function import ERC20Balance

# Load environment variables
load_dotenv()


def test_erc20_balance():
    # Initialize the ERC20Balance class
    erc20_balance = ERC20Balance()

    # Test parameters
    # Using USDC on Cronos zkEVM as an example
    test_params = {
        "address": "0x0a2989d3caa2d8955ddbe00bbf52d4ce00bb0b9e",  # Example wallet address
        "token_address": "0x18d40bd95e34d1a4fcaf9027db11f6988e5b860a",  # USDC on Cronos zkEVM
    }

    # Execute the function
    result = erc20_balance.execute(test_params, "", [])

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


if __name__ == "__main__":
    test_erc20_balance()
