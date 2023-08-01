import requests

# Takes an API key and returns the source-id of the merchant


def find_merchant_main(key):
    credential = "9A8D7D72-858D-44FF-A7F2-9BB06118BDF6"
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

