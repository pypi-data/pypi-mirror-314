import requests

from .api_interfaces import ApiResponse


def get_contract_abi(chain_id: str, api_key: str, contract_address: str) -> ApiResponse:
    """
    Get the ABI for a smart contract.

    :param chain_id: The ID of the blockchain network
    :param api_key: The API key for authentication.
    :param contract_address: The address of the smart contract.
    :return: The ABI of the smart contract.
    :rtype: ApiResponse
    :raises Exception: If the contract ABI retrieval fails or the server responds with an error.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/contract/{
        chain_id}/contract-abi?contractAddress={contract_address}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get('error') or
            f"""HTTP error! status: {response.status_code}"""
        )
        raise Exception(f"""Failed to fetch contract ABI: {
                        server_error_message}""")

    return response.json()
