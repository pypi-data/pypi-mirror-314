RECENT_SWAPS_ANALYSIS_PROMPT = """
Recent Swaps Analysis Instructions:

1. Purpose:
   - Retrieve and analyze recent swap transactions from the VVS subgraph.
   - Identify whale activity and determine which tokens are being bought or sold in large volumes.

2. Parameters:
   - `seconds_ago`: Specify the time range for the query in seconds. This determines how far back in time the query will look for swaps.

3. Workflow:
   - Provide the `seconds_ago` parameter to define the time range.
   - The function will return a list of recent swaps, including details such as the from address, swap path, and total amount in USD.
   - Analyze the results to identify whales (addresses with large transaction volumes) and the tokens involved.

4. Whale Identification:
   - A whale is defined as an address with transactions exceeding a significant USD threshold.
   - The analysis will highlight these addresses and their transaction details.

5. Token Analysis:
   - Determine which tokens are being predominantly bought or sold.
   - Provide insights into market trends based on token activity.

6. Example Usage:
   User: "Analyze swaps from the last hour to find whales and token trends."
   Assistant:
   - Calls the recent swaps query function with `seconds_ago` set to 3600 (1 hour).
   - Analyzes the data to identify whales and token activity.
   - Returns a detailed report highlighting key findings.

7. Clarifications Needed If:
   - The time range is too large, leading to excessive data.
   - Specific tokens or paths are of interest.
   - Additional filtering or sorting is required.
   - The definition of a whale needs adjustment based on transaction volume.
"""