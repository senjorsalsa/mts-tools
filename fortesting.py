import json
from tkinter import filedialog
import xml.etree.ElementTree as et


def test_main():
    with open(filedialog.askopenfilename(initialdir="C:\\Users\\victrosb\\Downloads"), encoding="utf-8") as inv_file:
        inv_file_json = json.load(inv_file)

    work_magic(inv_file_json)


def work_magic(data):
    namespace = "https://schemas.cdon.com/product/4.0/4.12.1/availability"
    marketplace = et.Element("marketplace", xmlns=namespace)
    for product in data["Products"]:
        if product.get("Stock") != 0:
            continue
        else:
            product_element = et.SubElement(marketplace, "product")
            et.SubElement(product_element, "id").text = str(product.get("SKU"))
            et.SubElement(product_element, "stock").text = str(product.get("Stock"))
            se = et.SubElement(product_element, "se")
            et.SubElement(se, "status").text = "Offline"
            delivery_time = et.SubElement(se, "deliveryTime")
            et.SubElement(delivery_time, "min").text = str(product.get("MinimumDeliveryTimeSe"))
            et.SubElement(delivery_time, "max").text = str(product.get("MaximumDeliveryTimeSe"))

    filename = input("Enter the filename to save: ")
    if not filename.endswith(".xml"):
        filename += ".xml"

    tree = et.ElementTree(marketplace)
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"The Availability file was completed and saved as \"{filename}\"")