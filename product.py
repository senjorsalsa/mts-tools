import xml.etree.ElementTree as et
import json
import os
from tkinter import filedialog

# NOT FINISHED

def product_main():
    json_inventory = get_json_inventory()
    non_variants, variants = divide_products_type(json_inventory)
    print(f"Products without variations: {len(non_variants)}\nVariations: {len(variants)}")
    # build_product_xml(json_inventory)


def divide_products_type(products):
    no_variants = []
    variants = []

    for product in products["Products"]:
        if product.get("ParentSKU") is None:
            no_variants.append(product)
        else:
            variants.append(product)
    return no_variants, variants


def get_json_inventory():
    json_inventory = open(filedialog.askopenfilename(initialdir=os.getcwd()), 'r', encoding="utf-8")
    json_content = json.load(json_inventory)
    json_inventory.close()
    return json_content


def build_product_xml(products):
    namespace = "https://schemas.cdon.com/product/4.0/4.9.0/product"
    marketplace = et.Element("marketplace", xmlns=namespace)
    for product in products["Products"]:
        prod = et.SubElement(marketplace, "product")
        identity = et.SubElement(prod, "identity")

        et.SubElement(identity, "id").text = str(product.get("SKU"))
        et.SubElement(identity, "gtin").text = str(product.get("Gtin"))

