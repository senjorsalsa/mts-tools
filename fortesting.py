import json
from tkinter import filedialog
import xml.etree.ElementTree as et
import PySimpleGUI as sg
import time


def test_main():
    layout = [
        [sg.Text('Progress')],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progress')],
        [sg.Button('Start'), sg.Button('Cancel')]
    ]

    window = sg.Window('Progress Bar Example', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Start':
            for i in range(100):
                window['progress'].update_bar(i + 1)
                time.sleep(0.1)

            sg.popup_animated(None)

    window.close()
