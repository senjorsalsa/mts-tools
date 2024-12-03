import json
import os
import openpyxl
import requests
import PySimpleGUI as sg
from tkinter import filedialog
import time

# NOT FINISHED

def kill_order_2_main():
    api_key = sg.popup_get_text("API key")
    json_data = get_orders_from_api(api_key)
    parse_orders(json_data)


def get_orders_from_api(key):
    header = {"Authorization": f"api {key}", "Content-Type": "application/xml"}
    link = "https://admin.marketplace.cdon.com/api/order"
    response = requests.get(url=link, headers=header)

    if response.status_code == 401:
        print("Unauthorized api key, check merchant status")
    elif response.status_code == 404:
        print("No orders found, check merchant orders")
    else:
        json_data = response.json()
        return json_data


def parse_orders(json_data):
    payload_to_cancel = []
    payload_picked_orders = []
    for order in json_data:
        payload_bit = {"OrderId": f"{order['OrderDetails'].get('OrderId')}", "Rows": []}

        for order_row in order["OrderDetails"]["OrderRows"]:
            payload_bit["Rows"].append({"OrderRowId": f"{order_row.get('OrderRowId')}", "QuantityToCancel": f"{order_row.get('Quantity')}"})

        if order["OrderDetails"]["OrderRows"][0].get('PickedQuantity') is None:
            payload_to_cancel.append(payload_bit)
        else:
            payload_picked_orders.append(payload_bit)


kill_order_2_main()
