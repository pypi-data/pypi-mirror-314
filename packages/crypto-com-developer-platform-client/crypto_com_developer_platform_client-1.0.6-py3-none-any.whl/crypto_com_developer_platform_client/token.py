from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.token_api import (
    get_erc20_token_balance,
    get_native_token_balance,
    swap_token,
    transfer_token,
    wrap_token,
)


class Token:
    """
    Token class for managing native token and ERC20 token operations.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Token class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_native_balance(cls, address: str) -> ApiResponse:
        """
        Get the native token balance for a given address.

        :param address: The address to get the balance for.
        :return: The balance of the native token.
        """
        chain_id = cls._client.get_chain_id()
        api_key = cls._client.get_api_key()
        return get_native_token_balance(chain_id, api_key, address)

    @classmethod
    def get_erc20_balance(cls, address: str, contract_address: str, block_height: str = "latest") -> ApiResponse:
        """
        Get the ERC20 token balance for a given address and contract address.

        :param address: The address to get the balance for.
        :param contract_address: The contract address to get the balance for.
        :param block_height: The block height to get the balance for.
        :return: The balance of the ERC20 token.
        """
        chain_id = cls._client.get_chain_id()
        api_key = cls._client.get_api_key()
        return get_erc20_token_balance(chain_id, api_key, address, contract_address, block_height)

    @classmethod
    def transfer_token(cls, to: str, amount: int, contract_address: str = '') -> ApiResponse:
        """
        Transfer a token to another address.

        :param to: The address to transfer the token to.
        :param amount: The amount of the token to transfer.
        :param contract_address: Optional. The contract address of the token to transfer.
        :return: The transaction hash.
        """
        chain_id = cls._client.get_chain_id()
        payload = {
            "to": to,
            "amount": amount,
            "provider": cls._client.get_provider(),
        }
        if contract_address:
            payload["contractAddress"] = contract_address
        return transfer_token(chain_id, payload)

    @classmethod
    def wrap_token(cls, amount: float) -> ApiResponse:
        """
        Wrap a token to another address.

        :param amount: The amount of the token to wrap.
        :return: The transaction hash.
        """
        chain_id = cls._client.get_chain_id()
        payload = {
            "amount": amount,
            "provider": cls._client.get_provider(),
        }

        return wrap_token(chain_id, payload)

    @classmethod
    def swap_token(cls, from_contract_address: str, to_contract_address: str, amount: int) -> ApiResponse:
        """
        Swap a token for another token.

        :param from_contract_address: The token to swap from.
        :param to_contract_address: The token to swap to.
        :param amount: The amount of the token to swap.
        :return: The transaction hash.
        """
        chain_id = cls._client.get_chain_id()
        payload = {
            "fromContractAddress": from_contract_address,
            "toContractAddress": to_contract_address,
            "amount": amount,
            "provider": cls._client.get_provider(),
        }

        return swap_token(chain_id, payload)
