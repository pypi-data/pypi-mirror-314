from datetime import datetime, timezone
from typing import Annotated

from eth_rpc import PrivateKeyWallet
from eth_rpc.networks import Network, get_network_by_name
from eth_typeshed.erc20 import ERC20
from eth_typeshed.uniswap_v2.router.contract import (
    EthSwapRequest,
    TokenSwapRequest,
    UniswapV2Router,
)
from eth_typing import HexAddress, HexStr
from typing_extensions import Doc

from .constants import ROUTER_ADDRESSES


async def swap_exact_tokens_for_tokens(
    token_in: Annotated[HexAddress, Doc("The token to swap from")],
    token_out: Annotated[HexAddress, Doc("The token to swap to")],
    amount_in: Annotated[float, Doc("The amount of tokens to swap")],
    recipient: Annotated[HexAddress, Doc("The recipient of the swapped tokens")],
    slippage: Annotated[float, Doc("The slippage tolerance")],
    deadline: Annotated[int | None, Doc("The deadline for the swap")],
    network: type[Network],
    wallet: PrivateKeyWallet,
) -> HexStr:
    if not deadline:
        deadline = int(datetime.now(timezone.utc).timestamp()) + 60
    assert deadline
    network_type = get_network_by_name(network)
    token = ERC20[network_type](address=token_in)
    decimals = await token.decimals().get()
    amount_in_wei = amount_in * 10**decimals
    router_address = ROUTER_ADDRESSES[network]
    router = UniswapV2Router[network_type](address=router_address)
    amount_out = await router.get_amounts_out(
        amount_in=amount_in_wei,
        path=[token_in, token_out],
    ).get()
    amount_out_min = amount_out[-1] * (1 - slippage)
    return await router.swap_exact_tokens_for_tokens_supporting_fee_on_transfer_tokens(
        TokenSwapRequest(
            amount_in=amount_in_wei,
            amount_out_min=amount_out_min,
            route=[
                token_in,
                token_out,
            ],
            to=recipient,
            deadline=deadline,
        )
    ).execute(wallet)


async def swap_exact_eth_for_tokens(
    token_out: HexAddress,
    amount_in: float,
    recipient: HexAddress,
    slippage: float,
    deadline: Annotated[int | None, Doc("The deadline for the swap")],
    network: type[Network],
    wallet: PrivateKeyWallet,
) -> HexStr:
    if not deadline:
        deadline = int(datetime.now(timezone.utc).timestamp()) + 60
    assert deadline
    decimals = 18
    amount_in_wei = amount_in * 10**decimals
    router_address = ROUTER_ADDRESSES[network]
    router = UniswapV2Router[network](address=router_address)
    weth_address = await router.weth().get()
    amount_out = await router.get_amounts_out(
        amount_in=amount_in_wei,
        path=[weth_address, token_out],
    ).get()
    amount_out_min = amount_out[-1] * (1 - slippage)
    return await router.swap_exact_eth_for_tokens_supporting_fee_on_transfer_tokens(
        EthSwapRequest(
            amount_out_min=amount_out_min,
            route=[
                weth_address,
                token_out,
            ],
            to=recipient,
            deadline=deadline,
        )
    ).execute(wallet, value=amount_in_wei)


async def swap_exact_tokens_for_eth(
    token_in: Annotated[HexAddress, Doc("The token to swap from")],
    amount_in: Annotated[float, Doc("The amount of tokens to swap")],
    recipient: Annotated[HexAddress, Doc("The recipient of the swapped tokens")],
    slippage: Annotated[float, Doc("The slippage tolerance")],
    deadline: Annotated[int | None, Doc("The deadline for the swap")],
    network: type[Network],
    wallet: PrivateKeyWallet,
) -> HexStr:
    if not deadline:
        deadline = int(datetime.now(timezone.utc).timestamp()) + 60
    assert deadline
    token = ERC20[network](address=token_in)
    decimals = await token.decimals().get()
    amount_in_wei = amount_in * 10**decimals
    router_address = ROUTER_ADDRESSES[network]
    router = UniswapV2Router[network](address=router_address)
    weth_address = await router.weth().get()
    amount_out = await router.get_amounts_out(
        amount_in=amount_in_wei,
        path=[token_in, weth_address],
    ).get()
    amount_out_min = amount_out[-1] * (1 - slippage)
    return await router.swap_exact_tokens_for_eth_supporting_fee_on_transfer_tokens(
        TokenSwapRequest(
            amount_in=amount_in_wei,
            amount_out_min=amount_out_min,
            route=[
                token_in,
                weth_address,
            ],
            to=recipient,
            deadline=deadline,
        )
    ).execute(wallet)
