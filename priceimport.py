from tkinter import filedialog
import json
import xml.etree.cElementTree as et

# Creates price.xml from a merchants inventory report in json format


def price_import_main():
    json_content = get_json_from_report()
    products_amount = build_price_xml(json_content)
    return products_amount


def get_json_from_report():
    json_inventory = open(filedialog.askopenfilename(), 'r', encoding="utf-8")
    json_content = json.load(json_inventory)
    json_inventory.close()
    return json_content


def build_price_xml(data):
    namespace = "https://schemas.cdon.com/product/4.0/4.9.0/price"
    marketplace = et.Element("marketplace", xmlns=namespace)
    i = 1
    for product in data["Products"]:
        product_element = et.SubElement(marketplace, "product")
        et.SubElement(product_element, "id").text = product["SKU"]

        if product.get("StatusSe") != "":
            se = et.SubElement(product_element, "se")
            et.SubElement(se, "salePrice").text = str(product.get("SalePriceSe"))
            et.SubElement(se, "originalPrice").text = str(product.get("OriginalPriceSe"))
            et.SubElement(se, "isShippedFromEU").text = "true"
            # if product.get("IsShippedFromEUSe"):
            #     et.SubElement(se, "isShippedFromEU").text = "true"
            # else:
            #     et.SubElement(se, "isShippedFromEU").text = "false"
            # et.SubElement(se, "shippingCost").text = str(product.get("ShippingCostSe"))
            et.SubElement(se, "shippingCost").text = "19"
            et.SubElement(se, "vat").text = str(product.get("VatSe"))

        if product.get("StatusDk") != "":
            dk = et.SubElement(product_element, "dk")
            et.SubElement(dk, "salePrice").text = str(product.get("SalePriceDk"))
            et.SubElement(dk, "originalPrice").text = str(product.get("OriginalPriceDk"))
            if product.get("IsShippedFromEUDk"):
                et.SubElement(dk, "isShippedFromEU").text = "true"
            else:
                et.SubElement(dk, "isShippedFromEU").text = "false"
            et.SubElement(dk, "shippingCost").text = str(product.get("ShippingCostDk"))
            et.SubElement(dk, "vat").text = str(product.get("VatDk"))

        if product.get("StatusNo") != "":
            no = et.SubElement(product_element, "no")
            et.SubElement(no, "salePrice").text = str(product.get("SalePriceNo"))
            et.SubElement(no, "originalPrice").text = str(product.get("OriginalPriceNo"))
            if product.get("IsShippedFromEUNo"):
                et.SubElement(no, "isShippedFromEU").text = "true"
            else:
                et.SubElement(no, "isShippedFromEU").text = "false"
            et.SubElement(no, "shippingCost").text = str(product.get("ShippingCostNo"))
            et.SubElement(no, "vat").text = str(product.get("VatNo"))

        if product.get("StatusFi") != "":
            fi = et.SubElement(product_element, "fi")
            et.SubElement(fi, "salePrice").text = str(product.get("SalePriceFi"))
            et.SubElement(fi, "originalPrice").text = str(product.get("OriginalPriceFi"))
            if product.get("IsShippedFromEUFi"):
                et.SubElement(fi, "isShippedFromEU").text = "true"
            else:
                et.SubElement(fi, "isShippedFromEU").text = "false"
            et.SubElement(fi, "shippingCost").text = str(product.get("ShippingCostFi"))
            et.SubElement(fi, "vat").text = str(product.get("VatFi"))
        i += 1

    tree = et.ElementTree(marketplace)
    tree.write("price.xml", encoding="utf-8", xml_declaration=True)
    return i
