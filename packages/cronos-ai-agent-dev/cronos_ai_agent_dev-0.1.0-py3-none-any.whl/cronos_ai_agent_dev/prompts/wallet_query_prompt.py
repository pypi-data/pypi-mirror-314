WALLET_QUERY_PROMPT = """
Wallet Query Instructions:

1. Implementation Paths:
   A. For a specific token:
      - Use get_native_balance for native CRO balance
      - Use get_erc20_balance for specific ERC20 token balance
      - Addresses are case-insensitive and will be converted to checksum format

   B. For full wallet overview:
      1. First get native CRO balance using get_native_balance
      2. Then get_h2_whitelist_tokens to list all available tokens
      3. Use get_erc20_balance for each token in the whitelist
      4. For each non-zero balance:
         - Get token price using appropriate price query path
         - Calculate USD value (token balance * token price)
      5. Present balances in format:
         Token: 10.5 CRO ($3.15)
         Token: 100 USDC ($100.00)
         Total Portfolio Value: $103.15

2. Workflow:
   If a specific token is mentioned:
   - For native CRO: Use get_native_balance
   - For ERC20 tokens: Use get_erc20_balance

   If no specific token is mentioned:
   - First get native CRO balance
   - Then get all H2 whitelist tokens
   - Check balance for each token
   - Present a comprehensive overview

3. Example Flow:
   User: "Show me the balance of 0x742d..."
   Assistant:
   - Gets native CRO balance
   - Gets H2 whitelist tokens
   - Checks each token balance
   - For non-zero balances:
     * Gets current token price
     * Calculates USD value
   - Returns formatted overview showing token amounts and USD values
   - Includes total portfolio value in USD

4. Clarifications Needed If:
   - Wallet address is ambiguous
   - Address format is invalid
   - Specific token request is unclear
   - Multiple matching tokens for a request
"""
