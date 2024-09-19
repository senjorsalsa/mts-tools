import requests
import os
from dotenv import load_dotenv

# Takes an API key and returns the source-id of the merchant


def find_merchant_main(key):
    load_dotenv("credentials.env")
    credential = os.getenv("API_KEY")
    headers = {"Authorization": f"api {credential}"}
    name = get_merchant(key, headers)

    if not name:
        return None

    return name


def get_merchant(key, h):
    url = f"https://admin.marketplace.cdon.com/api/merchant/{key}"
    response = requests.get(url, headers=h)

    if response.status_code != 200:
        return False
    else:
        json_response = response.json()
        return json_response.get("Name")

