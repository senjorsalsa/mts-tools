import requests
import json
import PySimpleGUI as sg
import findmerchant
import asyncio
import aiohttp


# Gathers the latest 1000 imported files for a merchant and generates a file with all errors found.
# A bit bad formatting for the resulting file though. No time to fix
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

    receipts_with_errors, unexpected_errors, error_messages = rinse_receipts(delivery_data)
    if len(receipts_with_errors) == 0:
        print("Could not find any import errors!")
        return
    elif len(receipts_with_errors) > 100:
        choice = sg.popup_yes_no("More than 100 receipts to fetch, proceed?")
        if choice == 'No':
            return

    normal_errors = get_errors_from_receipts(receipts_with_errors, key)
    normals_list = list(normal_errors)
    save_file(normals_list, name)


def get_api_key() -> str:
    return sg.popup_get_text("API key")


def get_initial_deliveries(h: dict):
    print("Gathering deliveries ...")
    raw_response = requests.get("https://mis.cdon.com/deliveries?take=1000", headers=h)
    if raw_response.status_code != 200:
        print("Issue fetching delivery errors")
        quit()

    return raw_response.json()


def rinse_receipts(data: list):
    error_messages = []
    failed_deliveries = []
    media_errors = []
    media_msg = "Unexpected error occurred. Please try importing again.\n"
    for part in data:
        part_status = part['status']
        if part_status != "Failed":
            continue
        if part_status == "Failed" and part['totalFailed'] == 0:
            error_messages.append(part['errorMessage'])
        elif part_status == "Failed" and part['endPoint'] != 'Media':
            failed_deliveries.append(part['receiptId'])
        else:
            media_errors.append(f"{part['endPoint']} - {part['receiptId']} - {media_msg}")
    return failed_deliveries, media_errors, error_messages


async def fetch_data(session, url, headers):
    async with session.get(url, headers=headers) as response:
        response_bytes = await response.read()
        response_text = response_bytes.decode('utf-8')
        return response_text


async def fetch_all_data(urls, headers):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url, headers) for url in urls]
        return await asyncio.gather(*tasks)


async def handle_request(urls, key):
    print(f'Fetching delivery errors, found {len(urls)}')
    headers = {"Authorization": f"api {key}"}
    results = await fetch_all_data(urls, headers)
    return results


def get_errors_from_receipts(receipts: list, key: str):
    urls = [f'https://mis.cdon.com/deliveries/{receipt}/failures' for receipt in receipts]
    problems = asyncio.run(handle_request(urls, key))
    return problems


def remove_slash(normal_list):
    transforms = {
        "\\": ""
    }
    new_list = []
    for each in normal_list:
        for key, value in transforms:
            new_list.append(each.replace(key, value))
    return new_list


def save_file(normals: list, name: str):
    with open(f"import errors\\{name} import errors.json", 'w', encoding='utf-8') as output:
        json.dump(normals, output, indent=4)
    print(f"File saved as '{name} import errors.json'")
