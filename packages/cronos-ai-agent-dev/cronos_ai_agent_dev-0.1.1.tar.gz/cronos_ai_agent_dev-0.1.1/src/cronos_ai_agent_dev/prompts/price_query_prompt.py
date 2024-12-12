PRICE_QUERY_PROMPT = """
Price Query Instructions:

1. Implementation Path:
   A. For H2 Finance tokens on Cronos zkEVM:
      - First use get_h2_whitelist_tokens to check if the token exists in H2 Finance
      - If found in the whitelist, use get_h2_token_price with the found address
      - This path is for tokens specifically on Cronos zkEVM through H2 Finance

   B. For general cryptocurrencies:
      - Use this path if the token is not found in H2 Finance whitelist
      - First use get_cryptocurrency_ids to find the correct coin ID
      - Then use get_cryptocurrency_price with the found ID
      - This path is for major cryptocurrencies like BTC, ETH, CRO

2. Workflow:
   - FIRST call get_h2_whitelist_tokens to check if the token exists in H2 Finance
   - If found in H2 whitelist: Use the H2 Finance price path
   - If not found in H2 whitelist: Use the general cryptocurrency path

3. Example Flow:
   User: "What's the price of TOKEN?"
   Assistant:
   - Calls get_h2_whitelist_tokens to check H2 Finance first
   - If found in H2: Uses get_h2_token_price
   - If not found in H2: Uses get_cryptocurrency_ids then get_cryptocurrency_price

4. Clarifications Needed If:
   - Token name is ambiguous
   - Multiple matching tokens are found
   - Token cannot be found in either system
   - Token symbol format is invalid
"""
