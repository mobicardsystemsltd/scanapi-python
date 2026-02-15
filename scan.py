import json
import base64
import hmac
import hashlib
import random
import requests
from urllib.parse import quote

# Mandatory claims
mobicard_version = "2.0"
mobicard_mode = "LIVE"  # production
mobicard_merchant_id = ""
mobicard_api_key = ""
mobicard_secret_key = ""

mobicard_token_id = str(random.randint(1000000, 1000000000))
mobicard_txn_reference = str(random.randint(1000000, 1000000000))
mobicard_service_id = "20000"  # Scan Card service ID
mobicard_service_type = "1"  # Use '1' for CARD SCAN METHOD 1
mobicard_extra_data = "your_custom_data_here_will_be_returned_as_is"

# Create JWT Header
jwt_header = {
    "typ": "JWT",
    "alg": "HS256"
}
jwt_header_encoded = base64.urlsafe_b64encode(json.dumps(jwt_header).encode()).decode().rstrip('=')

# Create JWT Payload
jwt_payload = {
    "mobicard_version": mobicard_version,
    "mobicard_mode": mobicard_mode,
    "mobicard_merchant_id": mobicard_merchant_id,
    "mobicard_api_key": mobicard_api_key,
    "mobicard_service_id": mobicard_service_id,
    "mobicard_service_type": mobicard_service_type,
    "mobicard_token_id": mobicard_token_id,
    "mobicard_txn_reference": mobicard_txn_reference,
    "mobicard_extra_data": mobicard_extra_data
}

jwt_payload_encoded = base64.urlsafe_b64encode(json.dumps(jwt_payload).encode()).decode().rstrip('=')

# Generate Signature
header_payload = f"{jwt_header_encoded}.{jwt_payload_encoded}"
signature = hmac.new(
    mobicard_secret_key.encode(),
    header_payload.encode(),
    hashlib.sha256
).digest()
jwt_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')

# Create Final JWT
mobicard_auth_jwt = f"{jwt_header_encoded}.{jwt_payload_encoded}.{jwt_signature}"

# Request Access Token
url = "https://mobicardsystems.com/api/v1/card_scan"
payload = {"mobicard_auth_jwt": mobicard_auth_jwt}

try:
    response = requests.post(url, json=payload, verify=False)
    response_data = response.json()
    
    if response_data.get('status_code') == "200":
        mobicard_transaction_access_token = response_data['mobicard_transaction_access_token']
        mobicard_token_id = response_data['mobicard_token_id']
        mobicard_scan_card_url = response_data['mobicard_scan_card_url']
        
        print("Access Token Generated Successfully!")
        print(f"Transaction Access Token: {mobicard_transaction_access_token}")
        print(f"Token ID: {mobicard_token_id}")
        print(f"Scan Card URL: {mobicard_scan_card_url}")
    else:
        print(f"Error: {response_data}")
        
except Exception as e:
    print(f"Request failed: {e}")
