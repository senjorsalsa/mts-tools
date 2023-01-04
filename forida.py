import openpyxl as xl
import json
from tkinter import filedialog
import os
import xml.etree.ElementTree as et


def idas_main():
    cwd = os.getcwd()
    workbook = get_workbook(cwd)
    orders = get_orders_from_excel(workbook)
    inventory_report_json = get_inventory_report(cwd)
    work_magic(orders, inventory_report_json)


def get_workbook(cwd):
    workbook = xl.load_workbook(filedialog.askopenfilename(initialdir=cwd))
    return workbook


def get_orders_from_excel(workbook):
    orders = []
    worksheet = workbook.worksheets[0]

    for row in range(2, worksheet.max_row + 1):
        orders.append({"OrderId": worksheet[f"A{row}"].value, "Price": worksheet[f"B{row}"].value})

    return orders


def get_inventory_report(cwd):
    json_file = open(filedialog.askopenfilename(initialdir=cwd))
    json_data = json.load(json_file)
    json_file.close()

    return json_data


def work_magic(orders, json_orders):
    namespace = "https://schemas.cdon.com/product/4.0/4.9.0/price"
    marketplace = et.Element("marketplace", xmlns=namespace)
    for order in orders:
        for inv_order in json_orders['Products']:
            if inv_order["CdonProductId"] != order["OrderId"]:
                continue

            product_element = et.SubElement(marketplace, "product")
            et.SubElement(product_element, "id").text = inv_order["SKU"]
            if inv_order.get("StatusSe") != "":
                se = et.SubElement(product_element, "se")
                et.SubElement(se, "salePrice").text = str(order.get("Price"))
                et.SubElement(se, "originalPrice").text = str(order.get("Price"))
                if inv_order.get("IsShippedFromEUSe"):
                    et.SubElement(se, "isShippedFromEU").text = "true"
                else:
                    et.SubElement(se, "isShippedFromEU").text = "false"
                et.SubElement(se, "shippingCost").text = str(inv_order.get("ShippingCostSe"))
                et.SubElement(se, "vat").text = str(inv_order.get("VatSe"))

    tree = et.ElementTree(marketplace)
    tree.write("price.xml", encoding="utf-8", xml_declaration=True)