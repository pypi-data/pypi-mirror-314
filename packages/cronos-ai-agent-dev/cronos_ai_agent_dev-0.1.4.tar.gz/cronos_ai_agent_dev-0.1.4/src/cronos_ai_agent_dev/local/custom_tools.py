from .base_tools import BaseTools
from ..functions.h2_token_price_function import function as h2_price_function
from ..functions.cronos_zkevm_knowledge_function import function as cronos_zkevm_knowledge_function
from ..functions.crypto_ids_function import function as crypto_ids_function
from ..functions.coingecko_price_function import function as crypto_price_function
from ..functions.cdc_agent_sdk_function import function as blockchain_data_function
from ..functions.h2_whitelist_function import function as h2_whitelist_function
from ..functions.native_balance_function import function as native_balance_function
from ..functions.erc20_balance_function import function as erc20_balance_function
from ..functions.vvs_recent_swaps_function import function as vvs_recent_swaps_function

class CustomTools(BaseTools):
    @property
    def register_functions(self):
        return [
            h2_price_function,
            cronos_zkevm_knowledge_function,
            crypto_ids_function,
            crypto_price_function,
            blockchain_data_function,
            h2_whitelist_function,
            native_balance_function,
            erc20_balance_function,
            vvs_recent_swaps_function,
        ]