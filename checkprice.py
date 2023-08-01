import PySimpleGUI as sg
import json
from tkinter import filedialog
import xml.etree.ElementTree as ET
import xmltodict
import os

# Compares prices from a price import file with prices from inventory report.

cwd = os.getcwd()


def price_main():
    layout = [[sg.Text('Open Inventory report first, then the import file')],
              [sg.Button('OK')]]

    window = sg.Window('Information', layout)
    event, values = window.read()

    if event == 'OK':
        window.close()

    inventory_report_file = open_json_file()
    import_file = open_xml_file()
    # print(import_file)
    compare_prices(inventory_report_file, import_file)


def open_json_file():
    json_inventory = open(filedialog.askopenfilename(initialdir=cwd), 'r', encoding="utf-8")
    json_content = json.load(json_inventory)
    json_inventory.close()
    return json_content


def open_xml_file():
    with open(filedialog.askopenfilename(initialdir=cwd), 'r') as f:
        xml_data = f.read()
    json_data = xmltodict.parse(xml_data)
    return json_data


def compare_prices(inventory_file, import_file):
    incorrect_prices_sku = []

    for product in import_file['marketplace']['product']:
        product_id = product.get('id')
        sale_price_from_import = int(float(product['se'].get('salePrice')))

        for inventory_product in inventory_file['Products']:
            inventory_id = inventory_product.get('SKU')
            sale_price_from_inventory = int(float(inventory_product.get('SalePriceSe')))

            if inventory_id != product_id:
                continue
            if sale_price_from_inventory == sale_price_from_import:
                break

            print(f"Product id: {product_id}")
            print(f"Price in import: {product['se'].get('salePrice')}, price from CDON: {inventory_product.get('SalePriceSe')}")
