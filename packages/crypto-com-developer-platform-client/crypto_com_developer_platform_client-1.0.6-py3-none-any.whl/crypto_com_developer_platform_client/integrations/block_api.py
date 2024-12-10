import requests

from .api_interfaces import ApiResponse


def get_block_by_tag(chain_id: str, api_key: str, block_tag: str, tx_detail: str) -> ApiResponse:
    """
    Get block by tag.

    :param chain_id: The ID of the blockchain network (e.g., Ethereum, Cronos).
    :param api_key: The API key for authentication.
    :param block_tag: The tag of the block to retrieve (e.g., "latest", "pending", "finalized").
    :param tx_detail: The detail level of transactions in the block (e.g., "full", "medium", "light").
    :return: The block data.
    :rtype: ApiResponse
    :raises Exception: If the block retrieval fails or the server responds with an error.
    """
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/block/{
        chain_id}/block-tag?blockTag={block_tag}&txDetail={tx_detail}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = (
            error_body.get('error') or
            f"""HTTP error! status: {response.status_code}"""
        )
        raise Exception(f"""Failed to fetch block by tag: {
                        server_error_message}""")

    return response.json()
