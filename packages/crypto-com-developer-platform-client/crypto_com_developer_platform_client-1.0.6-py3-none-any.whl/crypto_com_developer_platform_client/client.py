

class Client:
    """
    Client class for managing API key, chain ID and provider.
    """

    _api_key: str
    _chain_id: str
    _provider: str

    @classmethod
    def init(cls, api_key: str, chain_id: str, provider: str = "") -> None:
        """
        Initialize the client with API key and chain ID. Provider is optional.

        :param api_key: The API key for authentication.
        :param chain_id: The blockchain network ID.
        """

        cls._api_key = api_key
        cls._chain_id = chain_id
        cls._provider = provider

        from .block import Block
        from .contract import Contract
        from .token import Token
        from .transaction import Transaction
        from .wallet import Wallet
        from .exchange import Exchange
        
        Contract.init(cls())
        Wallet.init(cls())
        Block.init(cls())
        Transaction.init(cls())
        Token.init(cls())
        Exchange.init(cls())

    @classmethod
    def get_api_key(cls) -> str:
        """
        Get the API key.

        :return: The API key.
        :raises ValueError: If the API key is not set.
        """
        if cls._api_key is None:
            raise ValueError("API key is not set. Please set the API key.")

        return cls._api_key

    @classmethod
    def get_chain_id(cls) -> str:
        """
        Get the chain ID.

        :return: The chain ID.
        :raises ValueError: If the chain ID is not set.
        """
        if cls._chain_id is None:
            raise ValueError("Chain ID is not set. Please set the chain ID.")

        return cls._chain_id

    @classmethod
    def get_provider(cls) -> str:
        """
        Get the provider.

        :return: The provider.
        """
        if cls._provider is None:
            raise ValueError("Provider is not set. Please set the provider.")

        return cls._provider
