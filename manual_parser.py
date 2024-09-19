import PySimpleGUI as sg
import re
import pyperclip


# Takes a list of CDON product links and extracts product Id's or CID's

def parser_main():
    layout = [
        [sg.Multiline(size=(90,10), key="-INPUT-")],
        [sg.Button("Parse Product ID", key="parse_cdon"), sg.Push(), sg.Text("0", key="input_amount")],
        [sg.Button("Parse CID", key="parse_cid")],
        [sg.Multiline(size=(90,10), key="-OUTPUT-")],
        [sg.Button("Copy result", key="copy"), sg.Push(), sg.Text("0", key="output_amount")]
    ]

    window = sg.Window("Parser", layout)

    pid_pattern = r"p\d{8,}"
    cid_pattern = r"c\d{8,}"

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "parse_cdon":
            match_pattern(pid_pattern, values['-INPUT-'], window)
        elif event == "parse_cid":
            match_pattern(cid_pattern, values['-INPUT-'], window)
        elif event == "copy":
            pyperclip.copy(values["-OUTPUT-"])


def match_pattern(pattern, values, window):
    lines_array = values.splitlines()
    output_amount = 0
    window["input_amount"].update(len(lines_array))
    output_text = ""
    for item in lines_array:
        match = re.search(pattern, item)

        if match:
            output_amount += 1
            value = match.group()
            output_text += f"{value[1:]}\n"
            window["-OUTPUT-"].update(output_text)
            window["output_amount"].update(output_amount)
