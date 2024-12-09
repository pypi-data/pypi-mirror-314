from typing import Annotated, Literal

from eth_rpc.networks import get_network_by_name
from eth_typeshed.uniswap_v2.factory import GetPairRequest, UniswapV2Factory
from eth_typeshed.uniswap_v2.pair import UniswapV2Pair
from eth_typing import HexAddress
from typing_extensions import Doc

from .constants import FACTORY_ADDRESSES


async def get_price(
    network: Annotated[
        Literal["ethereum", "arbitrum", "base"],
        Doc("The network to query for price"),
    ],
    token_in: Annotated[HexAddress, Doc("The token to swap from")],
    token_out: Annotated[HexAddress, Doc("The token to swap to")],
) -> float:
    """Calculate the price of a token in terms of another token on UniswapV2"""

    factory_address = FACTORY_ADDRESSES[network]

    network_type = get_network_by_name(network)
    factory = UniswapV2Factory[network_type](address=factory_address)
    pair = await factory.get_pair(
        GetPairRequest(
            token_a=token_in,
            token_b=token_out,
        )
    ).get()
    return await UniswapV2Pair[network_type](address=pair.address).get_price(
        token0=True
    )
