from .client import Client
from .integrations.api_interfaces import ApiResponse
from .integrations.exchange_api import get_all_tickers, get_ticker_by_instrument


class Exchange:
    """
    Exchange class for managing Crypto.com Exchange-related operations like retrieving ticker information (Chain agnostic).
    """

    _client: Client

    @classmethod
    def init(cls, client: Client) -> None:
        """
        Initialize the Exchange class with a Client instance.

        :param client: An instance of the Client class.
        """
        cls._client = client

    @classmethod
    def get_all_tickers(cls) -> ApiResponse:
        """
        Get all tickers from the Crypto.com Exchange (Chain agnostic).

        :return: A list of all available tickers and their information.
        """
        return get_all_tickers()

    @classmethod
    def get_ticker_by_instrument(cls, instrument_name: str) -> ApiResponse:
        """
        Get ticker information for a specific instrument from the Crypto.com Exchange (Chain agnostic).

        :param instrument_name: The name of the instrument to get ticker information for.
        :return: Ticker information for the specified instrument.
        :raises ValueError: If instrument_name is None or empty.
        """
        if not instrument_name:
            raise ValueError("Instrument name is required")

        return get_ticker_by_instrument(instrument_name)
