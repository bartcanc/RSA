import PySimpleGUI as sg

def main():
    layout = [
        [sg.I(), sg.FileBrowse()],
        [sg.Ok(), sg.Cancel()]
    ]

    window = sg.Window("Wybierz plik wejściowy", layout)
    event, values = window.read()
    if event == 'Cancel':
        window.close()
    print(values)
    window.close()
    return values[0]