import requests

class AangaraaPay:
    def __init__(self, api_url, app_key):
        self.api_url = api_url
        self.app_key = app_key

    def initiate_payment(self, phone_number, amount, description, transaction_id, operator):
        payload = {
            'phone_number': phone_number,
            'amount': amount,
            'description': description,
            'app_key': self.app_key,
            'transaction_id': transaction_id,
            'operator': operator,
        }
        response = requests.post(f"{self.api_url}/direct_payment", json=payload)
        return response.json()

    def check_transaction_status(self, pay_token):
        payload = {
            'payToken': pay_token,
            'app_key': self.app_key,
        }
        response = requests.post(f"{self.api_url}/aangaraa_check_status", json=payload)
        return response.json()
