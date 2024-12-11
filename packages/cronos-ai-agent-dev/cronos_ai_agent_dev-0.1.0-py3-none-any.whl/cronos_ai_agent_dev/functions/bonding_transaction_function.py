from web3 import Web3
from .base_function import BaseFunction
import os
from typing import Optional, Dict
from web3_input_decoder import decode_function


# Function selectors
FUNCTION_SELECTOR_LAUNCH = "0x3c0b93aa"
FUNCTION_SELECTOR_BUY = "0x7deb6025"


class BondingTransactionFunction(BaseFunction):
    def __init__(self):
        super().__init__()
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("CRONOS_ZKEVM_RPC_URL")))
        self.bonding_abi = [
            {
                "inputs": [
                    {"name": "_name", "type": "string"},
                    {"name": "_ticker", "type": "string"},
                    {"name": "cores", "type": "uint8[]"},
                    {"name": "desc", "type": "string"},
                    {"name": "img", "type": "string"},
                    {"name": "urls", "type": "string[4]"},
                    {"name": "purchaseAmount", "type": "uint256"},
                ],
                "name": "launch",
                "outputs": [],
                "type": "function",
            },
            {
                "inputs": [
                    {"name": "amountIn", "type": "uint256"},
                    {"name": "tokenAddress", "type": "address"},
                ],
                "name": "buy",
                "outputs": [],
                "type": "function",
            },
        ]

    @property
    def name(self) -> str:
        return "bonding_transaction_function"

    @property
    def spec(self) -> Dict:
        return {
            "name": "bonding_transaction",
            "description": "Retrieves and decodes bonding transaction details from the blockchain",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_hash": {
                        "type": "string",
                        "description": "The transaction hash to analyze",
                    },
                    "contract_address": {
                        "type": "string",
                        "description": "The contract address involved in the transaction",
                    },
                },
                "required": ["transaction_hash", "contract_address"],
            },
        }

    def _decode_launch_data(self, decoded) -> dict:
        """Decode launch function parameters"""
        try:
            result = {
                "name": "",
                "ticker": "",
                "cores": [],
                "description": "",
                "image": "",
                "urls": [],
                "purchase_amount": "0",
                "formatted_purchase_amount": "0",
            }

            for type_str, name, value in decoded:
                if name == "_name":
                    result["name"] = value
                elif name == "_ticker":
                    result["ticker"] = value
                elif name == "cores":
                    result["cores"] = [str(core) for core in value]
                elif name == "desc":
                    result["description"] = value
                elif name == "img":
                    result["image"] = value
                elif name == "urls":
                    result["urls"] = value if isinstance(value, list) else []
                elif name == "purchaseAmount":
                    result["purchase_amount"] = str(value)
                    result["formatted_purchase_amount"] = str(self.w3.from_wei(value, "ether"))
            return result
        except Exception as e:
            logger.error(f"Error decoding launch data: {str(e)}")
            return {}

    def _decode_buy_data(self, decoded) -> dict:
        """Decode buy function parameters"""
        try:
            result = {"amount_in": "0", "formatted_amount_in": "0", "token_address": None}

            for type_str, name, value in decoded:
                if name == "amountIn":
                    result["amount_in"] = str(value)
                    result["formatted_amount_in"] = str(self.w3.from_wei(value, "ether"))
                elif name == "tokenAddress":
                    result["token_address"] = value
            return result
        except Exception as e:
            logger.error(f"Error decoding buy data: {str(e)}")
            return {}

    def _decode_input_data(self, input_data: str) -> dict:
        """Decode transaction input data"""
        try:
            decoded = decode_function(self.bonding_abi, input_data)
            function_selector = input_data[:10]

            if function_selector == FUNCTION_SELECTOR_LAUNCH:
                return self._decode_launch_data(decoded)
            elif function_selector == FUNCTION_SELECTOR_BUY:
                return self._decode_buy_data(decoded)
            return {}
        except Exception as e:
            logger.error(f"Error decoding input: {str(e)}")
            return {}

    def _validate_transaction_hash(self, tx_hash: str) -> Optional[str]:
        """Validate transaction hash format"""
        if not isinstance(tx_hash, str):
            return None

        clean_tx = tx_hash.lower().strip()
        if clean_tx.startswith("0x"):
            clean_tx = clean_tx[2:]

        if len(clean_tx) == 64 and all(c in "0123456789abcdef" for c in clean_tx):
            return f"0x{clean_tx}"

        return None

    def _format_transaction_response(
        self, tx_receipt: dict, block: dict, tx: dict, decoded_input: dict
    ) -> str:
        """Format transaction response message"""
        response = (
            f"Transaction Status: Success\n"
            f"Block Number: {tx_receipt['blockNumber']}\n"
            f"Gas Used: {tx_receipt['gasUsed']}\n"
            f"Timestamp: {block['timestamp']}\n"
            f"Value: {self.w3.from_wei(tx['value'], 'ether')} ETH\n"
            f"From: {tx['from']}\n"
            f"To: {tx['to']}"
        )

        if decoded_input:
            if "purchase_amount" in decoded_input:  # Launch transaction
                response += (
                    f"\n\nLaunch Parameters:"
                    f"\nName: {decoded_input.get('name', 'N/A')}"
                    f"\nTicker: {decoded_input.get('ticker', 'N/A')}"
                    f"\nCores: {', '.join(decoded_input.get('cores', []))}"
                    f"\nDescription: {decoded_input.get('description', 'N/A')}"
                    f"\nImage: {decoded_input.get('image', 'N/A')}"
                    f"\nURLs: {', '.join(decoded_input.get('urls', []))}"
                    f"\nPurchase: {decoded_input.get('formatted_purchase_amount', '0')} AGENTFUN"
                )
            elif "amount_in" in decoded_input:  # Buy transaction
                response += (
                    f"\n\nBuy Parameters:"
                    f"\nAmount In: {decoded_input.get('formatted_amount_in', '0')} ETH"
                    f"\nToken Address: {decoded_input.get('token_address', 'N/A')}"
                )

        return response

    def execute(self, function_arg: dict, message: str, history: list) -> dict:
        try:
            tx_hash = function_arg.get("transaction_hash")
            contract_address = function_arg.get("contract_address")

            valid_tx_hash = self._validate_transaction_hash(tx_hash)
            if not valid_tx_hash:
                return {"success": False, "response": f"Invalid transaction hash format: {tx_hash}"}

            checksum_contract = self.w3.to_checksum_address(contract_address)
            if not self.w3.is_address(checksum_contract):
                return {
                    "success": False,
                    "response": f"Invalid contract address format: {contract_address}",
                }

            try:
                tx_receipt = self.w3.eth.get_transaction_receipt(valid_tx_hash)
                if not tx_receipt:
                    return {
                        "success": True,
                        "response": "Transaction is still pending",
                        "data": {"status": "pending", "transaction_hash": valid_tx_hash},
                    }

                tx = self.w3.eth.get_transaction(valid_tx_hash)
                block = self.w3.eth.get_block(tx_receipt["blockNumber"])

                if tx_receipt["status"] == 1:
                    input_data = tx.get("input", "0x")
                    if isinstance(input_data, bytes):
                        input_data = input_data.hex()
                    if not input_data.startswith("0x"):
                        input_data = "0x" + input_data

                    decoded_input = {}
                    if len(input_data) > 2:
                        function_selector = input_data[:10]
                        if function_selector in [FUNCTION_SELECTOR_LAUNCH, FUNCTION_SELECTOR_BUY]:
                            decoded_input = self._decode_input_data(input_data)

                    response = self._format_transaction_response(
                        tx_receipt, block, tx, decoded_input
                    )

                    return {
                        "success": True,
                        "response": response,
                        "data": {
                            "status": "success",
                            "transaction_hash": valid_tx_hash,
                            "block_number": tx_receipt["blockNumber"],
                            "gas_used": tx_receipt["gasUsed"],
                            "timestamp": block["timestamp"],
                            "value": str(self.w3.from_wei(tx["value"], "ether")),
                            "from_address": tx["from"],
                            "to_address": tx["to"],
                            "transaction_data": decoded_input if decoded_input else None,
                        },
                    }
                else:
                    return {
                        "success": False,
                        "response": f"Transaction failed. Gas used: {tx_receipt['gasUsed']}",
                        "data": {
                            "status": "failed",
                            "transaction_hash": valid_tx_hash,
                            "gas_used": tx_receipt["gasUsed"],
                        },
                    }

            except Exception as contract_error:
                return {
                    "success": False,
                    "response": f"Error checking transaction: {str(contract_error)}",
                }

        except Exception as e:
            return {"success": False, "response": f"Unexpected error: {str(e)}"}


# Register the function
function = BondingTransactionFunction.register()
