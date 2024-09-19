import os

import requests
import pandas as pd
import PySimpleGUI as sg
from dotenv import load_dotenv

# fetch package carriers and save to file


def carriers_main():
    load_dotenv("credentials.env")
    h = {"Authorization": f"api {os.getenv('API_KEY_FOR_CARRIERS')}"}
    url = "https://admin.marketplace.cdon.com/api/packagecarrier"
    response = requests.get(url=url, headers=h)
    response_json = response.json()

    filename = "output.xlsx"
    df = pd.DataFrame(response_json)
    df.to_excel(filename, index=False)

    layout = [
        [sg.Text(f"Module has run and saved carriers as {filename}")]
    ]
    window = sg.Window("File saved", layout)
    while True:
        event, values = window.read()

        # noinspection PyUnresolvedReferences
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
