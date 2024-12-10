from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.wallet_api import create_wallet, get_balance


class Wallet:
    """
    Wallet class for managing wallet-related operations like creation and balance retrieval.
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Wallet class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def create_wallet(cls) -> ApiResponse:
        """
        Create a new wallet.

        :return: The address of the new wallet.
        """
        return create_wallet()

    @classmethod
    def get_balance(cls, address: str) -> ApiResponse:
        """
        Get the balance of a wallet.

        :param address: The address to get the balance for.
        :return: The balance of the wallet.
        """
        chain_id = cls._client.get_chain_id()
        api_key = cls._client.get_api_key()
        return get_balance(chain_id, address, api_key)
