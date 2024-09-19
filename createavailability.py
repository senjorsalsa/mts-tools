import json
import xml.etree.ElementTree as et
import openpyxl as xl
import os
import PySimpleGUI as sg
from tkinter import filedialog


# Create availability.xml with delivery times of your choosing


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

    products = parse_product_data(minimum, maximum)
    create_xml(products)


def parse_product_data(minimum, maximum):
    product_list = []

    with open(filedialog.askopenfilename(initialdir="C:\\Users\\victrosb\\Downloads"), encoding="utf-8") as json_report:
        json_data = json.load(json_report)

    for product in json_data["Products"]:
        curr_product = {"SKU": str(product.get("SKU")),
                        "deliveryTimes": {"minimum": str(minimum), "maximum": str(maximum)},
                        "status": {"sweden": product.get("StatusSe"),
                                   "denmark": product.get("StatusDk"),
                                   "norway": product.get("StatusNo"),
                                   "finland": product.get("StatusFi")},
                        "stock": str(product.get("Stock"))}
        product_list.append(curr_product)

    return product_list


def create_xml(products):
    print("Building Availability file ...")
    namespace = "https://schemas.cdon.com/product/4.0/4.12.1/availability"
    marketplace = et.Element("marketplace", xmlns=namespace)
    i = 0
    for product in products:
        product_element = et.SubElement(marketplace, "product")
        et.SubElement(product_element, "id").text = str(product["SKU"])
        et.SubElement(product_element, "stock").text = str(product["stock"])
        if product["status"].get("sweden") == "Online":
            se = et.SubElement(product_element, "se")
            et.SubElement(se, "status").text = "Online"
            delivery_time = et.SubElement(se, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product["deliveryTimes"].get("minimum"))
            et.SubElement(delivery_time, "max").text = str(product["deliveryTimes"].get("maximum"))
        if product["status"].get("denmark") == "Online":
            dk = et.SubElement(product_element, "dk")
            et.SubElement(dk, "status").text = "Online"
            delivery_time = et.SubElement(dk, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product["deliveryTimes"].get("minimum"))
            et.SubElement(delivery_time, "max").text = str(product["deliveryTimes"].get("maximum"))
        if product["status"].get("norway") == "Online":
            no = et.SubElement(product_element, "no")
            et.SubElement(no, "status").text = "Online"
            delivery_time = et.SubElement(no, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product["deliveryTimes"].get("minimum"))
            et.SubElement(delivery_time, "max").text = str(product["deliveryTimes"].get("maximum"))
        if product["status"].get("finland") == "Online":
            fi = et.SubElement(product_element, "fi")
            et.SubElement(fi, "status").text = "Online"
            delivery_time = et.SubElement(fi, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product["deliveryTimes"].get("minimum"))
            et.SubElement(delivery_time, "max").text = str(product["deliveryTimes"].get("maximum"))
        i += 1
    tree = et.ElementTree(marketplace)
    tree.write("availability.xml", encoding="utf-8", xml_declaration=True)
    print("The Availability file was completed")
    print(f"Amount of products in file: {i}")
