import PySimpleGUI as sg

def main(event):
    layout = [
        [sg.I(), sg.FileBrowse()],
        [sg.Ok(), sg.Cancel()]
    ]

    if event == 'Generowanie kluczy RSA':
        window = sg.Window("Wybierz plik z losowymi bitami", layout)
    elif event == 'Szyfrowanie pliku':
        window = sg.Window("Wybierz plik do zaszyfrowania", layout)
    event, values = window.read()
    if event == 'Cancel':
        window.close()
    window.close()
    return values[0]