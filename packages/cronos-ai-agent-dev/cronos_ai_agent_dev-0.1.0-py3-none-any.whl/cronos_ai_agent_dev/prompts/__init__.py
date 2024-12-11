from .recent_swaps_analysis_prompt import RECENT_SWAPS_ANALYSIS_PROMPT
from .core_prompt import CORE_PROMPT
from .price_query_prompt import PRICE_QUERY_PROMPT
from .wallet_query_prompt import WALLET_QUERY_PROMPT
from .common_prompt import COMMON_PROMPT
from cachetools import cached, TTLCache

# Create cache with 1 hour TTL
instructions_cache = TTLCache(maxsize=1, ttl=3600)


@cached(cache=instructions_cache)
def get_full_instructions():
    return "\n\n".join(
        [
          CORE_PROMPT,
          COMMON_PROMPT,
          PRICE_QUERY_PROMPT,
          WALLET_QUERY_PROMPT,
          RECENT_SWAPS_ANALYSIS_PROMPT,
        ]
    )
