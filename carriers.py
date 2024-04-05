import requests
import pandas as pd
import PySimpleGUI as sg

# fetch package carriers and save to file
def carriers_main():
    h = {"Authorization": "api 3895a4ee-6f7a-4510-9422-e8a56de4e841"}
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
