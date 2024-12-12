import os
import requests
import time
from collections import defaultdict
from tabulate import tabulate
import curses

GRAPHQL_URL = "https://graph.cronoslabs.com/subgraphs/name/vvs/exchange"
MINIMUM_AMOUNT_USD = 5000
SECONDS_AGO = 1800
TABLE_MIN_ROWS = 5

def build_graphql_query(timestamp):
    return """
    {
      swaps(
        where: { timestamp_gte: %d }
        orderBy: timestamp
        orderDirection: desc
        first: 1000
      ) {
        amountUSD
        token0 {
          symbol
        }
        token1 {
          symbol
        }
        transaction {
          id
          timestamp
          block
        }
        from
        to
        amount0In
        amount1Out
        amount0Out
        amount1In
        id
        logIndex
      }
    }
    """ % timestamp

def retrieve_swaps(url, query):
    response = requests.post(url, json={'query': query})
    data = response.json()
    if 'errors' in data:
        print("Errors:", data['errors'])
        return []
    return data['data']['swaps']

def organize_transactions(swaps):
    transactions = defaultdict(list)
    for swap in swaps:
        transactions[swap['transaction']['id']].append(swap)
    return transactions

def compute_paths_and_totals(transactions):
    total_swaps = defaultdict(float)
    path_totals = defaultdict(float)
    path_details = defaultdict(lambda: {'addresses': defaultdict(float), 'transactions': []})

    for tx_id, tx_swaps in transactions.items():
        tx_swaps.sort(key=lambda x: x['logIndex'])
        path = []
        for swap in tx_swaps:
            if float(swap['amount0In']) == 0:
                path.extend([swap['token1']['symbol'], swap['token0']['symbol']])
            elif float(swap['amount1In']) == 0:
                path.extend([swap['token0']['symbol'], swap['token1']['symbol']])

        # Use only the first and last tokens to form the path
        full_path = f"{path[0]} -> {path[-1]}"

        # Calculate the total amount USD considering reverse paths
        total_amount_usd = 0
        for swap in tx_swaps:
            if path[0] == swap['token0']['symbol'] and path[-1] == swap['token1']['symbol']:
                total_amount_usd += float(swap['amountUSD'])
            elif path[0] == swap['token1']['symbol'] and path[-1] == swap['token0']['symbol']:
                total_amount_usd -= float(swap['amountUSD'])

        key = (tx_swaps[0]['from'], full_path)
        total_swaps[key] += total_amount_usd
        path_totals[full_path] += total_amount_usd

        # Track addresses and their bought volume
        path_details[full_path]['addresses'][tx_swaps[0]['from']] += total_amount_usd
        # Store each swap transaction for verification
        path_details[full_path]['transactions'].extend(tx_swaps)
    return total_swaps, path_totals, path_details

def filter_and_sort_totals(total_swaps, path_totals):
    sorted_total_swaps = sorted(total_swaps.items(), key=lambda item: item[1], reverse=True)
    sorted_path_totals = sorted(path_totals.items(), key=lambda item: item[1], reverse=True)

    # Filter based on the minimum amount, but ensure at least top 3 are included
    filtered_swaps_totals = [(path, total_amount) for path, total_amount in sorted_total_swaps if total_amount >= MINIMUM_AMOUNT_USD]
    filtered_path_totals = [(path, total_amount) for path, total_amount in sorted_path_totals if total_amount >= MINIMUM_AMOUNT_USD]

    if len(filtered_swaps_totals) < TABLE_MIN_ROWS:
        filtered_swaps_totals = sorted_total_swaps[:TABLE_MIN_ROWS]
    if len(filtered_path_totals) < TABLE_MIN_ROWS:
        filtered_path_totals = sorted_path_totals[:TABLE_MIN_ROWS]

    # Merge the last 5 items to show the most sell path and addresses
    merged_swaps_totals = sorted_total_swaps[-TABLE_MIN_ROWS:]
    merged_path_totals = sorted_path_totals[-TABLE_MIN_ROWS:]

    # Combine the merged items with the filtered ones
    filtered_swaps_totals.extend(merged_swaps_totals)
    filtered_path_totals.extend(merged_path_totals)

    return filtered_swaps_totals, filtered_path_totals

def display_merged_tables_curses(stdscr, filtered_swaps_totals, filtered_path_totals):
    stdscr.clear()

    # Get the current time and format it
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # Prepare data for the merged table
    merged_table_data = []

    # Add a header row for the swaps table
    merged_table_data.append(["From Address", "Path", "Total Amount USD", "", "Path", "Total Amount USD"])

    # Determine the maximum number of rows to display
    max_rows = max(len(filtered_swaps_totals), len(filtered_path_totals))

    # Fill the merged table with data from both tables
    for i in range(max_rows):
        swap_row = filtered_swaps_totals[i] if i < len(filtered_swaps_totals) else ("", "", "")
        path_row = filtered_path_totals[i] if i < len(filtered_path_totals) else ("", "")

        # Append the combined row
        merged_table_data.append([
            swap_row[0][0] if swap_row[0] else "",  # From Address
            swap_row[0][1] if swap_row[0] else "",  # Path
            swap_row[1] if swap_row[0] else "",     # Total Amount USD
            "",                                     # Separator
            path_row[0],                            # Path
            path_row[1]                             # Total Amount USD
        ])

    # Use tabulate to format the merged table
    merged_table = tabulate(merged_table_data, headers="firstrow", tablefmt="pretty")

    # Display the timestamp and the merged table
    stdscr.addstr(0, 0, f"Updated at: {current_time}\n")
    stdscr.addstr(1, 0, "Merged Table of Swaps and Paths:\n" + merged_table)
    stdscr.refresh()

def display_top_path_details(path_details, top_path):
    addresses = path_details[top_path]['addresses']
    transactions = path_details[top_path]['transactions']

    print(f"\nDetails for top path: {top_path}")
    print("Addresses and their bought volume:")

    # Sort addresses by volume in descending order
    sorted_addresses = sorted(addresses.items(), key=lambda item: item[1], reverse=True)
    for address, volume in sorted_addresses:
        print(f"Address: {address}, Volume: {volume}")

    print("\nTransactions for verification:")

    # Sort transactions by timestamp
    sorted_transactions = sorted(transactions, key=lambda tx: int(tx['transaction']['timestamp']))
    for transaction in sorted_transactions:
        tx_id = transaction['transaction']['id']
        timestamp = int(transaction['transaction']['timestamp'])  # Convert to integer
        amount_usd = transaction['amountUSD']
        token0 = transaction['token0']['symbol']
        token1 = transaction['token1']['symbol']
        amount0_in = transaction['amount0In']
        amount1_in = transaction['amount1In']
        amount0_out = transaction['amount0Out']
        amount1_out = transaction['amount1Out']

        print(f"Transaction ID: {tx_id}")
        print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestamp))}")
        print(f"Amount USD: {amount_usd}")
        print(f"Tokens: {token0} -> {token1}")
        print(f"Amounts In: {amount0_in} {token0}, {amount1_in} {token1}")
        print(f"Amounts Out: {amount0_out} {token0}, {amount1_out} {token1}")
        print("-" * 40)

def main(stdscr):
    while True:
        one_hour_ago = int(time.time()) - SECONDS_AGO
        query = build_graphql_query(one_hour_ago)
        swaps = retrieve_swaps(GRAPHQL_URL, query)
        print(f"Number of swaps retrieved: {len(swaps)}")
        transactions = organize_transactions(swaps)
        total_swaps, path_totals, path_details = compute_paths_and_totals(transactions)
        filtered_swaps_totals, filtered_path_totals = filter_and_sort_totals(total_swaps, path_totals)
        display_merged_tables_curses(stdscr, filtered_swaps_totals, filtered_path_totals)

        # # Get the top path
        # if filtered_path_totals:
        #     top_path = filtered_path_totals[0][0]
        #     display_top_path_details(path_details, top_path)

        # Wait for a specified interval before refreshing
        time.sleep(10)  # Refresh every 60 seconds

if __name__ == "__main__":
    curses.wrapper(main)