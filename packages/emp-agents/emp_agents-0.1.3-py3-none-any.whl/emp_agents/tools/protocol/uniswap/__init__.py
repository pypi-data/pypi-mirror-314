import json
from typing import Annotated, Callable, Literal

from eth_rpc import PrivateKeyWallet
from eth_rpc.networks import Network
from eth_typing import HexAddress
from typing_extensions import Doc

from emp_agents.implicits import IgnoreDepends, Provider, inject
from emp_agents.models.protocol import SkillSet, onchain_action, view_action

from ..network import NetworkSkill
from ..wallets import SimpleWalletSkill
from .price import get_price
from .swap import (
    swap_exact_eth_for_tokens,
    swap_exact_tokens_for_eth,
    swap_exact_tokens_for_tokens,
)

uniswap_scope = Provider()


def load_wallet() -> PrivateKeyWallet | None:
    """
    This can be overridden by using the scope for your agent.
    Use `scope_load_wallet` to scope this method.
    """
    return SimpleWalletSkill.get_wallet()


def load_network() -> type[Network] | None:
    """
    This can be overridden by using the scope for your agent.
    Use `scope_load_network` to scope this method.
    """
    return NetworkSkill.get_network_type()


def scope_load_wallet(
    new_load_wallet: Callable[..., PrivateKeyWallet]
) -> tuple[Provider, Callable, Callable]:
    return (uniswap_scope, load_wallet, new_load_wallet)


class UniswapSkill(SkillSet):
    """
    Skills for interacting with UniswapV2.
    """

    @view_action
    @staticmethod
    @inject(dependency_overrides_provider=uniswap_scope)
    async def get_price(
        network: Annotated[
            Literal["ethereum", "arbitrum", "base"],
            Doc("The network to query for price"),
        ],
        token_in: Annotated[HexAddress, Doc("The token to swap from")],
        token_out: Annotated[HexAddress, Doc("The token to swap to")],
    ) -> str:
        """Get the price of a token in terms of another token on UniswapV2"""

        price = await get_price(network, token_in, token_out)
        return json.dumps({"price": str(price)})

    @onchain_action
    @staticmethod
    @inject(dependency_overrides_provider=uniswap_scope)  # type: ignore[call-overload]
    async def swap(
        input_token: Annotated[
            HexAddress | None, Doc("The token to swap from.  None if ETH")
        ],
        output_token: Annotated[
            HexAddress | None, Doc("The token to swap to. None if ETH")
        ],
        amount_in: Annotated[float, Doc("The amount of tokens to swap")],
        recipient: Annotated[HexAddress, Doc("The recipient of the swapped tokens")],
        slippage: Annotated[
            float, Doc("The slippage tolerance, defaults to 0.5%")
        ] = 0.005,
        deadline: Annotated[
            int | None,
            Doc("The deadline for the swap, defaults to 1 minute from now"),
        ] = None,
        network: type[Network] | None = IgnoreDepends(load_network),
        wallet: PrivateKeyWallet | None = IgnoreDepends(load_wallet),
    ) -> str:
        """Swap an exact amount of tokens for ETH.  Returns the transaction hash or error message."""

        if wallet is None:
            return "WalletNotFoundError: make sure you have setup your wallet loading logic"

        if network is None:
            return "NetworkNotFoundError: make sure you have setup your network loading logic"

        if input_token is None:
            if output_token is None:
                return "InvalidSwapError: both input and output tokens cannot be None"
            assert output_token is not None
            return await swap_exact_eth_for_tokens(
                output_token,
                amount_in,
                recipient,
                slippage,
                deadline,
                network,
                wallet,
            )
        elif output_token is None:
            return await swap_exact_tokens_for_eth(
                input_token,
                amount_in,
                recipient,
                slippage,
                deadline,
                network,
                wallet,
            )
        return await swap_exact_tokens_for_tokens(
            input_token,
            output_token,
            amount_in,
            recipient,
            slippage,
            deadline,
            network,
            wallet,
        )
