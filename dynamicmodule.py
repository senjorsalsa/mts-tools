import json
import os
from tkinter import filedialog
import openpyxl as xl


def dynamic_main():
    json_data = get_json_data()
    stock_zero, stock_above_zero = do_the_magic(json_data)
    print(f"Amount of products with zero stock: {stock_zero}\nAmount above zero stock: {stock_above_zero}")


def get_json_data():
    with open(filedialog.askopenfilename(initialdir=os.getcwd()), encoding="utf-8") as json_report:
        json_data = json.load(json_report)
    return json_data


def do_the_magic(dataset):
    amount = 0
    zero = 0
    for product in dataset["Products"]:
        if product.get("Stock") > 0:
            amount += 1
        else:
            zero += 1
    return zero, amount
