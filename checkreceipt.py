import json
import requests
import PySimpleGUI as sg


def checkreceipt_main():
    layout = [
        [sg.Text("Enter API key"), sg.InputText(key="-APIKEY-")],
        [sg.Text("Input Receipt Ids")],
        [sg.Multiline(size=(90,10), key="-INPUT-")],
        [sg.Button("Submit", key="-SUBMIT-")]
    ]

    window = sg.Window("Check Receipt Ids", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        if event == "-SUBMIT-":
            receipt_ids = parse_receipt_ids(values)
            make_requests(receipt_ids, values)


def parse_receipt_ids(values):
    return [d for d in values.get("-INPUT-").split('\n')]


def make_requests(receipts, values):
    api_key = values.get("-APIKEY-")
    url = "https://mis.cdon.com/deliveries/"
    headers = {
        "Authorization": f"api {api_key}"
    }

    receipt_responses = []
    for receipt in receipts:
        response = requests.get(url=url + receipt, headers=headers)
        receipt_responses.append(response.json())

    for x in receipt_responses:
        print(f"{x.get('receiptId')} - {x.get('endPoint')}\nStatus: {x.get('status')}\n")

checkreceipt_main()