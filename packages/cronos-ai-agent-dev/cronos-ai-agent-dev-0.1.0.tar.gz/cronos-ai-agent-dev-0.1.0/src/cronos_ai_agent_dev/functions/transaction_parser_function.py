from web3 import Web3
from typing import Dict, Any, Optional, List

# Constants for native tokens by chain ID
NATIVE_SYMBOL_BY_CHAIN_ID = {
    1: "ETH",  # Ethereum Mainnet
    56: "BNB",  # Binance Smart Chain
    137: "MATIC",  # Polygon
    # Add other chain IDs and symbols as needed
}

NATIVE_TOKEN_ADDRESS = "0x0000000000000000000000000000000000000000"
ERC_4337_ENTRY_POINT = "0xYourERC4337EntryPointAddress"  # Replace with actual address
MULTICALL3_ADDRESS = "0xYourMulticall3Address"  # Replace with actual address
FUNCTION_SELECTORS = {
    'EXECUTE_META_TXN': '0xYourFunctionSelector'  # Replace with actual selector
}

# Function to check if a chain ID is supported
def is_chain_id_supported(chain_id: int) -> bool:
    supported_chain_ids = [1, 56, 137]  # Add other supported chain IDs
    return chain_id in supported_chain_ids

# Function to calculate native token transfer
def calculate_native_transfer(trace: List[Dict[str, Any]], recipient: str, direction: str = "to") -> str:
    total_transferred = 0
    recipient_lower = recipient.lower()

    def process_call(call: Dict[str, Any]):
        nonlocal total_transferred
        if 'value' not in call or call['value'] == '0x':
            return

        relevant_address = call['from'] if direction == "from" else call['to']
        if relevant_address.lower() == recipient_lower:
            total_transferred += int(call['value'], 16)

    def traverse_calls(calls: List[Dict[str, Any]]):
        for call in calls:
            process_call(call)
            if 'calls' in call and call['calls']:
                traverse_calls(call['calls'])

    traverse_calls(trace)
    return Web3.fromWei(total_transferred, 'ether')

# Function to parse smart contract wallet transactions
def parse_smart_contract_wallet_tx(logs: List[Dict[str, Any]], trace: List[Dict[str, Any]], chain_id: int, smart_contract_wallet: str):
    smart_contract_wallet_transfer_logs = {'output': None, 'input': None}

    for log in logs:
        if log['to'] == smart_contract_wallet:
            smart_contract_wallet_transfer_logs['output'] = log
        if log['from'] == smart_contract_wallet:
            smart_contract_wallet_transfer_logs['input'] = log

    input_log = smart_contract_wallet_transfer_logs['input']
    output_log = smart_contract_wallet_transfer_logs['output']

    native_amount_to_taker = calculate_native_transfer(trace, smart_contract_wallet)
    native_amount_from_taker = calculate_native_transfer(trace, smart_contract_wallet, direction="from")

    if not output_log and native_amount_to_taker != "0":
        if input_log:
            return {
                'tokenIn': {
                    'address': input_log['address'],
                    'amount': input_log['amount'],
                    'symbol': input_log['symbol'],
                },
                'tokenOut': {
                    'address': NATIVE_TOKEN_ADDRESS,
                    'amount': native_amount_to_taker,
                    'symbol': NATIVE_SYMBOL_BY_CHAIN_ID[chain_id],
                },
            }
        else:
            return None

    if not input_log and native_amount_from_taker != "0":
        wrapped_native_asset = "WBNB" if chain_id == 56 else "WMATIC" if chain_id == 137 else "WETH"
        input_log = next((log for log in logs if log['symbol'] == wrapped_native_asset), None)

        if input_log and output_log:
            return {
                'tokenIn': {
                    'address': NATIVE_TOKEN_ADDRESS,
                    'amount': input_log['amount'],
                    'symbol': NATIVE_SYMBOL_BY_CHAIN_ID[chain_id],
                },
                'tokenOut': {
                    'address': output_log['address'],
                    'amount': output_log['amount'],
                    'symbol': output_log['symbol'],
                },
            }
        else:
            return None

    if input_log and output_log:
        return {
            'tokenIn': {
                'address': input_log['address'],
                'amount': input_log['amount'],
                'symbol': input_log['symbol'],
            },
            'tokenOut': {
                'address': output_log['address'],
                'amount': output_log['amount'],
                'symbol': output_log['symbol'],
            },
        }

    return None

# Function to parse swap transactions
async def parse_swap(public_client, transaction_hash: str, smart_contract_wallet: Optional[str] = None):
    chain_id = await public_client.get_chain_id()

    if not is_chain_id_supported(chain_id):
        raise ValueError(f"chainId {chain_id} is unsupported")

    trace = await public_client.trace_transaction(transaction_hash)
    transaction = await public_client.get_transaction(transaction_hash)

    taker = transaction['from']
    value = transaction['value']
    to = transaction['to']

    is_to_erc4337 = to.lower() == ERC_4337_ENTRY_POINT.lower()

    native_amount_to_taker = calculate_native_transfer(trace, recipient=taker)

    transaction_receipt = await public_client.get_transaction_receipt(transaction_hash)

    is_native_sell = value > 0

    logs = await transfer_logs(public_client, transaction_receipt)

    if is_to_erc4337:
        if not smart_contract_wallet:
            raise ValueError("This is an ERC-4337 transaction. You must provide a smart contract wallet address.")

        return parse_smart_contract_wallet_tx(logs, trace, chain_id, smart_contract_wallet)

    from_taker = [log for log in logs if log['from'].lower() == taker.lower()]

    input_log = from_taker[0] if from_taker else logs[0]

    output_log = (
        logs[-1] if native_amount_to_taker == "0" else {
            'symbol': NATIVE_SYMBOL_BY_CHAIN_ID[chain_id],
            'amount': native_amount_to_taker,
            'address': NATIVE_TOKEN_ADDRESS,
        }
    )

    if to.lower() == MULTICALL3_ADDRESS.lower():
        multicall_args = decode_function_data(multicall3Abi, transaction['input'])
        settler_args = decode_function_data(SETTLER_META_TXN_ABI, multicall_args[0][1]['callData'])

        taker_for_gasless_approval_swap = settler_args[0]['recipient'].lower()

        native_amount_to_taker = calculate_native_transfer(trace, recipient=taker_for_gasless_approval_swap)

        if native_amount_to_taker == "0":
            output_log = logs[-1]
        else:
            output_log = {
                'symbol': NATIVE_SYMBOL_BY_CHAIN_ID[chain_id],
                'amount': native_amount_to_taker,
                'address': NATIVE_TOKEN_ADDRESS,
            }

    if transaction['input'].startswith(FUNCTION_SELECTORS['EXECUTE_META_TXN']):
        args = decode_function_data(SETTLER_META_TXN_ABI, transaction['input'])
        msg_sender = args[3]

        native_amount_to_taker = calculate_native_transfer(trace, recipient=msg_sender)

        if native_amount_to_taker == "0":
            output_log = logs[-1]
            taker_received = [log for log in logs if log['to'].lower() == msg_sender.lower()]
            if len(taker_received) == 1:
                output_log = {
                    'symbol': taker_received[0]['symbol'],
                    'amount': taker_received[0]['amount'],
                    'address': taker_received[0]['address'],
                }
            else:
                output_log = {'symbol': "", 'amount': "", 'address': ""}
                print("File a bug report here, including the expected results (URL to a block explorer) and the unexpected results.")

            input_log = [log for log in logs if log['from'].lower() == msg_sender.lower()][0]
        else:
            output_log = {
                'symbol': NATIVE_SYMBOL_BY_CHAIN_ID[chain_id],
                'amount': native_amount_to_taker,
                'address': NATIVE_TOKEN_ADDRESS,
            }

    if is_native_sell:
        native_sell_amount = Web3.fromWei(value, 'ether')
        token_out = {
            'symbol': "",
            'amount': "",
            'address': ""
        }
        for log in logs:
            if log['to'].lower() == taker:
                token_out = {
                    'symbol': log['symbol'],
                    'amount': Web3.fromWei(int(log['amount']), 'ether'),
                    'address': log['address'],
                }

        return {
            'tokenIn': {
                'symbol': NATIVE_SYMBOL_BY_CHAIN_ID[chain_id],
                'address': NATIVE_TOKEN_ADDRESS,
                'amount': native_sell_amount,
            },
            'tokenOut': token_out,
        }

    if not output_log:
        print("File a bug report here, including the expected results (URL to a block explorer) and the unexpected results.")
        return None

    return {
        'tokenIn': {
            'symbol': input_log['symbol'],
            'amount': input_log['amount'],
            'address': input_log['address'],
        },
        'tokenOut': {
            'symbol': output_log['symbol'],
            'amount': output_log['amount'],
            'address': output_log['address'],
        },
    }

async def transfer_logs(public_client, transaction_receipt) -> List[Dict[str, Any]]:
    EVENT_SIGNATURES = {
        "Transfer": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
    }

    transfer_logs = [
        log for log in transaction_receipt['logs']
        if log['topics'][0] == EVENT_SIGNATURES["Transfer"]
    ]

    enriched_logs = []
    for log in transfer_logs:
        address = log['address']
        data = log['data']
        topics = log['topics']

        # Decode the log data and topics
        from_address = Web3.toChecksumAddress('0x' + topics[1][26:])
        to_address = Web3.toChecksumAddress('0x' + topics[2][26:])
        amount = Web3.fromWei(int(data, 16), 'ether')

        enriched_logs.append({
            'from': from_address,
            'to': to_address,
            'amount': amount,
            'address': address,
        })

    return enriched_logs