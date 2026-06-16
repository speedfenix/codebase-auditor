import requests
import os

# Retrieve the Stripe API key from an environment variable
# It is crucial that this environment variable is set in the production environment
# and not committed to version control.
API_KEY = os.getenv("STRIPE_API_KEY")

if not API_KEY:
    raise ValueError("STRIPE_API_KEY environment variable not set. Cannot process payments securely.")

def process_payment(amount, currency="USD"):
    print(f"💰 Processing payment of {amount} {currency} via Stripe.")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"amount": amount, "currency": currency}
    # This call now uses the key retrieved from environment variables
    response = requests.post("https://api.stripe.com/v1/charges", headers=headers, json=payload)
    return response.json()