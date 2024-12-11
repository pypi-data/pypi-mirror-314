# Zaz Aangaraa Pay Python Package

A Python package for integrating MTN and Orange Money payments in Cameroon.

## Installation

```bash
pip install zaz_aangaraa_pay_python
```

## Usage

```python
from zaz_aangaraa_pay_python import AangaraaPay

api_url = 'https://your-api-url.com/api'
app_key = 'your_app_key'
payment = AangaraaPay(api_url, app_key)

response = payment.initiate_payment('237600000000', 1000, 'Test Payment', 'unique_transaction_id', 'MTN_Cameroon')
print(response)
```

## Check Payment Status

```python
from aangaraa_pay import AangaraaPay

api_url = 'https://your-api-url.com/api'
app_key = 'your_app_key'
payment = AangaraaPay(api_url, app_key)


response = payment.check_transaction_status('YOUR_PAY_TOKEN')
print(response)
```

## License

This project is licensed under the MIT License.
