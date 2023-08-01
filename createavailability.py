import json
import xml.etree.ElementTree as et
import openpyxl as xl
import os
import PySimpleGUI as sg
from tkinter import filedialog

# Create availability.xml with dynamic delivery times


def custom_availability_main():
    layout = [
        [sg.Text('Enter minimum and maximum delivery time')],
        [sg.Text('Min', size=(5, 1)), sg.InputText()],
        [sg.Text('Max', size=(5, 1)), sg.InputText()],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Delivery time data', layout)
    event, values = window.read()
    window.close()
    minimum = values[0]
    maximum = values[1]
    cwd = os.getcwd()

    products = get_merchant_products_xl(cwd, minimum, maximum)
    create_xml(products)


def get_merchant_products_xl(cwd, minimum, maximum):
    products = []
    workbook = xl.load_workbook(filedialog.askopenfilename(initialdir=cwd))
    worksheet = workbook.worksheets[0]

    with open(filedialog.askopenfilename(initialdir=cwd), encoding="utf-8") as json_report:
        json_data = json.load(json_report)

    for row in range(2, worksheet.max_row + 1):
        position = worksheet.cell(row, 1)
        bit = {}

        for product_dict in json_data["Products"]:
            if product_dict["CdonProductId"] == position.value:
                bit["sku"] = product_dict["SKU"]
                bit["minimum"] = worksheet.cell(row, 5).value
                bit["maximum"] = worksheet.cell(row, 6).value
                bit["status"] = worksheet.cell(row, 4).value
                if bit["status"] == "Offline":
                    bit["stock"] = 0
                else:
                    bit["stock"] = product_dict["Stock"]
                products.append(bit)
                break

    return products


def create_xml(products):
    print("Building Availability file ...")
    namespace = "https://schemas.cdon.com/product/4.0/4.12.1/availability"
    marketplace = et.Element("marketplace", xmlns=namespace)
    i = 0
    for product in products:
        product_element = et.SubElement(marketplace, "product")
        et.SubElement(product_element, "id").text = str(product["sku"])
        et.SubElement(product_element, "stock").text = str(product["stock"])
        se = et.SubElement(product_element, "se")
        # et.SubElement(se, "status").text = str(product.get("StatusSe"))
        et.SubElement(se, "status").text = product["status"]
        delivery_time = et.SubElement(se, "deliveryTime")
        et.SubElement(delivery_time, "min").text = str(product["minimum"])
        et.SubElement(delivery_time, "max").text = str(product["maximum"])
        i += 1
    tree = et.ElementTree(marketplace)
    tree.write("availability_kristinas_online.xml", encoding="utf-8", xml_declaration=True)
    print("The Availability file was completed")
    print(f"Amount of products in file: {i}")
