import json
import PySimpleGUI as sg
import openpyxl as xl
from tkinter import filedialog

# checks an inventory report and marks any GTIN that appears twice

def gtin_main():
    layout = [[sg.Text('Choose if the inventory report is Excel or JSON format')],
              [sg.Button('Excel', key='Excel')],
              [sg.Button('JSON', key='JSON')]]

    window = sg.Window('Information', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        match event:
            case 'Excel':
                file_excel_check()
                break
            case 'JSON':
                file_json_check()
                break


def file_excel_check():
    workbook = xl.load_workbook(filedialog.askopenfilename(initialdir="C:\\Users\\victrosb\\Downloads"))
    active_sheet = workbook.worksheets[0]

    for row in range(1, active_sheet.max_row + 1):
        pass
        # unfinished


def file_json_check():
    with open(filedialog.askopenfilename(initialdir="C:\\Users\\victrosb\\Downloads"), encoding="utf-8") as json_file:
        json_content = json.load(json_file)
    gtin_list = []
    duplicate = []
    for product in json_content["Products"]:
        gtin = product.get("Gtin")
        if gtin in gtin_list and gtin is not None:
            duplicate.append({"gtin": gtin, "sku": product.get("SKU"), "product status": {"sweden": product.get("StatusSe"),
                                                                                          "denmark": product.get("StatusDk"),
                                                                                          "norway": product.get("StatusNo"),
                                                                                          "finland": product.get("StatusFi")}})
        else:
            gtin_list.append(gtin)

    print(duplicate)
