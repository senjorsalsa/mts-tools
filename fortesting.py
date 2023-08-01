import json
from tkinter import filedialog
import os

result = []
def testingmain():
    with open("gs.json", encoding="utf-8") as f:
        json_gs = json.load(f)
    cwd = os.getcwd()

    json_inventory = open(filedialog.askopenfilename(initialdir=cwd), "r", encoding="utf-8")
    json_data = json.load(json_inventory)
    json_inventory.close()

    for product in json_gs["products"]:
        for inv_product in json_data["Products"]:
            if inv_product.get("SKU") == product:
                result.append(inv_product.get("CdonProductId"))

    print(result)