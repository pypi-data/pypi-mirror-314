from typing import Any, Dict

import requests

from .api_interfaces import ApiResponse


def create_wallet() -> ApiResponse:
    """
    Creates a new wallet using the API.

    :return: The newly created wallet information.
    :rtype: ApiResponse
    :raises Exception: If the wallet creation fails or the server responds with an error.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/wallet"""

    try:
        response = requests.post(
            url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if response.status_code not in (200, 201):
            error_body = response.json()
            error_message = error_body.get('error') or f"""HTTP error! status: {
                response.status_code}"""
        raise Exception(f"""Failed to create wallet: {error_message}""")


def get_balance(chain_id: str, address: str, api_key: str) -> ApiResponse:
    """
    Fetches the native token balance of a wallet.

    :param chain_id: The ID of the blockchain network
    :param address: The wallet address to check the balance for
    :return: The native token balance of the wallet.
    :rtype: ApiResponse
    :raises Exception: If the fetch request fails or the server responds with an error message.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/wallet/{
        chain_id}/balance?address={address}&apiKey={api_key}"""

    try:
        response = requests.get(
            url, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_message = str(e)
        if response.status_code not in (200, 201):
            error_body = response.json()
            error_message = error_body.get('error') or f"""HTTP error! status: {
                response.status_code}"""
        raise Exception(f"""Failed to fetch wallet balance: {error_message}""")
