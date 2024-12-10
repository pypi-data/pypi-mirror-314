import requests

from .api_interfaces import ApiResponse


def get_transactions_by_address(chain_id: str, address: str, session: str, limit: str, api_key: str) -> ApiResponse:
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/transaction/{
        chain_id}/address?address={address}&session={session}&limit={limit}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch transactions by address: {
                        server_error_message}""")

    return response.json()


def get_transaction_by_hash(chain_id: str, tx_hash: str, api_key: str) -> ApiResponse:
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/transaction/{
        chain_id}/tx-hash?txHash={tx_hash}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch transaction by hash: {
                        server_error_message}""")

    return response.json()


def get_transaction_status(chain_id: str, tx_hash: str, api_key: str) -> ApiResponse:
    url = f"""https://developer-platform-api.crypto.com/v1/cdc-developer-platform/transaction/{
        chain_id}/status?txHash={tx_hash}&apiKey={api_key}"""

    response = requests.get(url, headers={'Content-Type': 'application/json'})

    if response.status_code not in (200, 201):
        error_body = response.json()
        server_error_message = error_body.get('error') or f"""HTTP error! status: {
            response.status_code}"""
        raise Exception(f"""Failed to fetch transaction status: {
                        server_error_message}""")

    return response.json()
