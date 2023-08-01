import json
import PySimpleGUI as sg
import os
import openpyxl as xl


def gtin_main():
    cwd = os.getcwd()
    layout = [[sg.Text('Choose if the file is Excel or JSON format')],
              [sg.Button('Excel')],
              [sg.button('JSON')]]

    window = sg.Window('Information', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Excel':
            file_excel_check()
        elif event == 'JSON':
            file_json_check()


def file_excel_check():
    workbook = xl.load_workbook(filedialog.askopenfilename(initialdir=os.getcwd()))
    active_sheet = workbook.worksheets[0]

    for row in range(1, active_sheet.max_row + 1):
        pass


def file_json_check():
    pass