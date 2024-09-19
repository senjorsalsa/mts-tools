import PySimpleGUI as sg
import html

# Paste text you want to clean up, will change some HTML entities to their respective characters.


def convert_main():
    layout = [
        [sg.Text("Paste Text Here:")],
        [sg.Multiline(key="input_text", size=(90, 10))],
        [sg.Button("Convert"), sg.Exit()],
        [sg.Text("Converted text")],
        [sg.Multiline(size=(90, 10), key="output_text")]
    ]

    window = sg.Window("Text Converter", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        elif event == "Convert":
            input_text = values["input_text"]
            converted_text = convert_text(input_text)
            window["output_text"].update(converted_text)

    window.close()


def convert_text(input_text):
    conversions = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&ouml;": "ö",
        "&aring;": "å",
        "&auml;": "ä",
        "&quot;": "\""
    }

    for key, value in conversions.items():
        input_text = input_text.replace(key, value)

    return input_text
