import requests

from .api_interfaces import ApiResponse


def get_all_tickers() -> ApiResponse:
    """
    Get all tickers from the Crypto.com Exchange (Chain agnostic).

    :return: A list of all available tickers and their information.
    :raises Exception: If the ticker retrieval fails or the server responds with an error.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/exchange/tickers"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get('error') or
            f"HTTP error! status: {response.status_code}"
        )
        raise Exception(f"Failed to fetch all tickers: {server_error_message}")

    return response.json()


def get_ticker_by_instrument(instrument_name: str) -> ApiResponse:
    """
    Get ticker information for a specific instrument from the Crypto.com Exchange (Chain agnostic).

    :param instrument_name: The name of the instrument to get ticker information for.
    :return: Ticker information for the specified instrument.
    :raises Exception: If the ticker retrieval fails, does not exist or the server responds with an error.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/exchange/tickers/{
        instrument_name}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get('error') or
            f"HTTP error! status: {response.status_code}"
        )
        raise Exception(f"""Failed to fetch ticker for instrument {
                        instrument_name}: {server_error_message}""")

    return response.json()
