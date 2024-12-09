import json
from contextvars import ContextVar
from typing import Dict, Optional

import aiohttp

BASE_URL: ContextVar[str] = ContextVar(
    "base_url", default="https://api.dexscreener.com"
)


class DexScreenerApi:
    """API client for DexScreener"""

    @staticmethod
    async def search_pairs(query: str) -> str:
        """Search for pairs matching query"""
        url = f"{BASE_URL.get()}/latest/dex/search"
        params = {"q": query}
        return await DexScreenerApi._make_request(url, params=params)

    @staticmethod
    async def get_pair_by_chain(chain_id: str, pair_id: str) -> str:
        """Get pairs by chain and pair address"""
        url = f"{BASE_URL.get()}/latest/dex/pairs/{chain_id}/{pair_id}"
        return await DexScreenerApi._make_request(url)

    @staticmethod
    async def find_pairs_by_tokens(token_addresses: list[str]) -> str:
        """Get pairs by token addresses"""
        addresses = ",".join(token_addresses[:30])
        url = f"{BASE_URL.get()}/latest/dex/tokens/{addresses}"
        return await DexScreenerApi._make_request(url)

    @staticmethod
    async def get_token_profiles() -> str:
        """Get the latest token profiles"""
        url = f"{BASE_URL.get()}/token-profiles/latest/v1"
        return await DexScreenerApi._make_request(url)

    @staticmethod
    async def get_latest_boosted_tokens() -> str:
        """Get the latest boosted tokens"""
        url = f"{BASE_URL.get()}/token-boosts/latest/v1"
        return await DexScreenerApi._make_request(url)

    @staticmethod
    async def get_top_boosted_tokens() -> str:
        """Get the tokens with most active boosts"""
        url = f"{BASE_URL.get()}/token-boosts/top/v1"
        return await DexScreenerApi._make_request(url)

    @staticmethod
    async def get_orders_by_token(chain_id: str, token_address: str) -> str:
        """Get orders by chain and token address"""
        url = f"{BASE_URL.get()}/orders/v1/{chain_id}/{token_address}"
        return await DexScreenerApi._make_request(url)

    @staticmethod
    async def _make_request(url: str, params: Optional[Dict] = None) -> str:
        """Helper method to make HTTP requests"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    r = await response.json()
                    return json.dumps(r)
                else:
                    error_response = {
                        "error": f"Request failed with status {response.status}",
                        "details": await response.text(),
                    }
                    return json.dumps(error_response)
