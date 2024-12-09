from contextvars import ContextVar
from typing import Annotated, Optional

from eth_rpc import Account, PrivateKeyWallet
from eth_rpc.networks import Network, get_network_by_name
from eth_typing import HexAddress, HexStr
from typing_extensions import Doc

from emp_agents.implicits import Depends, inject
from emp_agents.models.protocol import SkillSet, onchain_action, tool_method

from ..network import NetworkOptions, NetworkSkill

# Context variable to store private key
_private_key: ContextVar[Optional[str]] = ContextVar("_private_key", default=None)


class SimpleWalletSkill(SkillSet):
    """A simple wallet tool that stores private key in memory using context vars"""

    @staticmethod
    def get_wallet() -> PrivateKeyWallet:
        key = _private_key.get()
        if key is None:
            raise ValueError("No private key set")
        return PrivateKeyWallet(private_key=HexStr(key))

    @tool_method
    @staticmethod
    def create_wallet() -> str:
        """Create a new private key wallet"""

        wallet = PrivateKeyWallet.create_new()
        _private_key.set(wallet.private_key)
        return (
            f"Wallet created: {wallet.address} with private key: {wallet.private_key}"
        )

    @tool_method
    @staticmethod
    def set_private_key(
        private_key: Annotated[str, Doc("The private key to set")]
    ) -> str:
        """Set the private key in the context"""

        _private_key.set(private_key)
        return "Private key set successfully"

    @tool_method
    @staticmethod
    def get_private_key() -> str:
        """Get the private key from the context"""

        key = _private_key.get()
        if key is None:
            return "No private key set"
        return key

    @tool_method
    @staticmethod
    def clear_private_key() -> str:
        """Clear the private key from the context"""

        _private_key.set(None)
        return "Private key cleared"

    @tool_method
    @staticmethod
    def get_address() -> str:
        """Get the address of the wallet"""

        key = _private_key.get()
        if key is None:
            return "No private key set"
        wallet = PrivateKeyWallet(private_key=HexStr(key))
        return wallet.address

    @tool_method
    @staticmethod
    @inject
    async def get_eth_balance(
        address: Annotated[
            HexAddress, Doc("The address to get the balance of")
        ] = Depends(get_address),
        network: Annotated[
            NetworkOptions | None,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
    ) -> str:
        """Get the balance of the wallet in ETH"""

        if network is None:
            return "No network set, try setting the network first"

        network_type: type[Network] = get_network_by_name(network)
        balance = await Account[network_type].get_balance(address)  # type: ignore[valid-type]
        return f"Balance: {balance}"

    @onchain_action
    @staticmethod
    @inject
    async def transfer_eth(
        recipient: Annotated[HexAddress, Doc("The address to transfer the ETH to")],
        amount: Annotated[int, Doc("The amount of ETH to transfer, in wei")],
        message: Annotated[
            str | None,
            Doc(
                "Any data you want to include in the transfer.  It will be utf-8 encoded"
            ),
        ] = None,
        network: Annotated[
            NetworkOptions | None,
            Doc("The network to use"),
        ] = Depends(NetworkSkill.get_network_str),
    ) -> str:
        """Transfer ETH to a recipient"""

        if network is None:
            return "No network set, try setting the network first"
        wallet = SimpleWalletSkill.get_wallet()
        if wallet is None:
            return "No wallet set, try creating a wallet first"

        network_type: type[Network] = get_network_by_name(network)
        balance = await Account[network_type].get_balance(wallet.address)  # type: ignore[valid-type]
        if message:
            data = "0x" + message.encode("utf-8").hex()
        else:
            data = "0x"

        if balance <= amount:
            return "Insufficient balance"

        tx = await wallet[network_type].transfer(recipient, amount, data=data)
        return f"Transaction sent: {tx}"
