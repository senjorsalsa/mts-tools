import openpyxl as xl
from tkinter import filedialog
import xml.etree.ElementTree as et


def idas_main():
    product_excel = xl.load_workbook(filedialog.askopenfilename(initialdir="C:\\Users\\victrosb\\Downloads"))
    ws = product_excel.worksheets[0]

    sku_list = [ws.cell(row, 1).value for row in range(2, ws.max_row + 1)]

    namespace = "https://schemas.cdon.com/product/4.0/4.12.1/availability"
    marketplace = et.Element("marketplace", xmlns=namespace)

    for product in sku_list:
        product_element = et.SubElement(marketplace, "product")
        et.SubElement(product_element, "id").text = str(product)
        et.SubElement(product_element, "stock").text = "0"

        se = et.SubElement(product_element, "se")
        et.SubElement(se, "status").text = "Offline"
        delivery_time = et.SubElement(se, "deliveryTime")
        et.SubElement(delivery_time, "min").text = "1"
        et.SubElement(delivery_time, "max").text = "3"

    filename = input("Enter the filename to save: ")
    if not filename.endswith(".xml"):
        filename += ".xml"

    tree = et.ElementTree(marketplace)
    tree.write(filename, encoding="utf-8", xml_declaration=True)




idas_main()