import xml.etree.ElementTree as et
import os
import json
from tkinter import filedialog


def availability_import_main():
    json_content = get_json_from_report()
    build_availability_xml(json_content)


def get_json_from_report():
    cwd = os.getcwd()
    json_inventory = open(filedialog.askopenfilename(initialdir=cwd), 'r', encoding="utf-8")
    json_content = json.load(json_inventory)
    json_inventory.close()
    return json_content


def build_availability_xml(data):
    print("Building Availability file ...")
    namespace = "https://schemas.cdon.com/product/4.0/4.12.1/availability"
    marketplace = et.Element("marketplace", xmlns=namespace)
    i = 1
    for product in data["Products"]:
        product_element = et.SubElement(marketplace, "product")
        et.SubElement(product_element, "id").text = str(product.get("SKU"))
        et.SubElement(product_element, "stock").text = str(product.get("Stock"))

        if product.get("StatusSe") != "":
            se = et.SubElement(product_element, "se")
            et.SubElement(se, "status").text = str(product.get("StatusSe"))
            delivery_time = et.SubElement(se, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product.get("MinimumDeliveryTimeSe"))
            et.SubElement(delivery_time, "max").text = str(product.get("MaximumDeliveryTimeSe"))

        if product.get("StatusDk") != "":
            dk = et.SubElement(product_element, "dk")
            et.SubElement(dk, "status").text = str(product.get("StatusDk"))
            delivery_time = et.SubElement(dk, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product.get("MinimumDeliveryTimeDk"))
            et.SubElement(delivery_time, "max").text = str(product.get("MaximumDeliveryTimeDk"))

        if product.get("StatusNo") != "":
            no = et.SubElement(product_element, "no")
            et.SubElement(no, "status").text = str(product.get("StatusNo"))
            # et.SubElement(no, "status").text = "Offline"
            # et.SubElement(no, "status").text = "Online"
            delivery_time = et.SubElement(no, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product.get("MinimumDeliveryTimeNo"))
            et.SubElement(delivery_time, "max").text = str(product.get("MaximumDeliveryTimeNo"))

        if product.get("StatusFi") != "":
            fi = et.SubElement(product_element, "fi")
            et.SubElement(fi, "status").text = str(product.get("StatusFi"))
            delivery_time = et.SubElement(fi, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product.get("MinimumDeliveryTimeFi"))
            et.SubElement(delivery_time, "max").text = str(product.get("MaximumDeliveryTimeFi"))
        i += 1
    tree = et.ElementTree(marketplace)
    tree.write("availability.xml", encoding="utf-8", xml_declaration=True)
    print("The Availability file was completed")
    print(f"Amount of products in file: {i}")
