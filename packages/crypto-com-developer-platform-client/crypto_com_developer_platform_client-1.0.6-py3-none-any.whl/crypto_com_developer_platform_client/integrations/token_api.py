from typing import Optional

import requests

from .api_interfaces import ApiResponse


def get_native_token_balance(chain_id: str, api_key: str, address: str) -> ApiResponse:
    """
    Get the native token balance for a given address.

    :param chain_id: The ID of the blockchain network
    :param api_key: The API key for authentication.
    :param address: The address to check the balance for.
    :return: The native token balance.
    :rtype: ApiResponse
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/token/{
        chain_id}/native-token-balance?address={address}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch native token balance: {
                        server_error_message}""")

    return response.json()


def get_erc20_token_balance(chain_id: str, api_key: str, address: str, contract_address: str, block_height: str) -> ApiResponse:
    """
    Get the ERC20 token balance for a given address.

    :param chain_id: The ID of the blockchain network
    :param api_key: The API key for authentication.
    :param address: The address to check the balance for.
    :param contract_address: The address of the ERC20 token contract.
    :param block_height: The block height to check the balance at.
    :return: The ERC20 token balance.
    :rtype: ApiResponse
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/token/{
        chain_id}/erc20-token-balance?address={
        address}&contractAddress={contract_address}&blockHeight={block_height}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch ERC20 token balance: {
                        server_error_message}""")

    return response.json()


def transfer_token(chain_id: str, payload: dict) -> ApiResponse:
    """
    Transfer a token.

    :param chain_id: The ID of the blockchain network
    :param payload: The payload for the transfer.
    :param provider: The provider for the transfer.
    :return: The transfer response.
    """
    url = f"https://developer-platform-api.crypto.com/v1/cdc-developer-platform/token/{
        chain_id}/transfer"

    response = requests.post(
        url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to transfer token: {
                        server_error_message}""")

    return response.json()


def wrap_token(chain_id: str, payload: dict) -> ApiResponse:
    """
    Wrap a token.

    :param chain_id: The ID of the blockchain network
    :param payload: The payload for the wrap.
    :param provider: The provider for the wrap.
    :return: The wrap response.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/token/{
        chain_id}/wrap"""

    response = requests.post(
        url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to wrap token: {server_error_message}""")

    return response.json()


def swap_token(chain_id: str, payload: dict) -> ApiResponse:
    """
    Swap a token.

    :param chain_id: The ID of the blockchain network
    :param payload: The payload for the swap.
    :param provider: The provider for the swap.
    :return: The swap response.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/token/{
        chain_id}/swap"""

    response = requests.post(
        url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to swap token: {server_error_message}""")

    return response.json()
