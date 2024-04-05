import requests
import json
import PySimpleGUI as sg
import findmerchant


# Gathers the last 1000 imported files for a merchant and generates a text file with all errors.
def delivery_main():
    key = ""
    while key == "" or len(key) != 36:
        key = get_api_key()
    h = {"Authorization": f"api {key}"}

    name = findmerchant.find_merchant_main(key)
    delivery_data = get_initial_deliveries(h)

    if not delivery_data:
        print("Unable to get deliveries! There were either no deliveries to fetch, or the API key was incorrect")
        quit()
    receipts_with_errors, unexpected_errors = rinse_receipts(delivery_data)
    if len(receipts_with_errors) == 0:
        print("Could not find any import errors!")
        return
    elif len(receipts_with_errors) > 100:
        print(f"There are over 100 receipts with errors ({len(receipts_with_errors)})")
        r = input("Fetch all errors? (Y/N): ")
        if r.lower() == "n":
            quit()
    normal_errors = get_errors_from_receipts(receipts_with_errors, h)
    save_file(normal_errors, unexpected_errors, name)


def get_api_key():
    return sg.popup_get_text("API key")


def get_initial_deliveries(h: dict):
    print("Gathering deliveries ...")
    raw_response = requests.get("https://mis.cdon.com/deliveries?take=1000", headers=h)
    if raw_response.status_code != 200:
        return False

    return raw_response.json()


def rinse_receipts(data: list):
    list_of_deliveries_with_errors = [part.get('receiptId') for part in data if part.get("status") == "Failed"]
    media_errors = []
    for part in data:
        part_status = part.get("status")
        part_error = part.get("errorMessage")
        if part.get("status") != "Failed":
            continue
        if part_status == "Failed" and part_error.startswith("Unexpected"):
            media_errors.append(f"{part.get('endPoint')} - {part.get('receiptId')} - Unexpected error occured. Please try importing again.\n")
            continue
    return list_of_deliveries_with_errors, media_errors


def get_errors_from_receipts(receipts: list, h: dict):
    problems = []
    i = 0
    for receipt in receipts:
        i += 1
        print(f"Fetching {i} of {len(receipts)}")
        response = requests.get(f"https://mis.cdon.com/deliveries/{receipt}/failures", headers=h)
        response_json = response.json()
        for each in response_json:
            try:
                each["receiptId"] = receipt
            except TypeError:
                print(f"Woopsie, type error, some issue with {receipt}")
        problems.append(response_json)
    return problems


def save_file(normals: list, unexpected: list, name: str):
    with open(f"import errors\\{name} import errors.txt", 'w', encoding='utf-8') as output:
        for each in normals:
            json.dump(each, output, indent=4)
        output.writelines(unexpected)
    print(f"File saved as '{name} import errors.txt'")


def get_merchant_name(key):

    url = f"https://admin.marketplace.cdon.com/api/merchant/{key}"
    response = requests.get(url, headers=hdr)
    json_response = response.json()
    return json_response.get("Name")
