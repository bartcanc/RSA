import PySimpleGUI as sg

def main(message):
    if message == 'code':
        layout = [
            [sg.Text("Najpierw wygeneruj klucze RSA!")],
            [sg.Button('Wróć')]
        ]
    elif message == 'decode':
        layout = [
            [sg.Text("Najpierw zaszyfruj plik!")],
            [sg.Button('Wróć')]
        ]
    elif message == 'none':
        layout = [
            [sg.Text("Brak plików do usunięcia.")],
            [sg.Button('Wróć')]
        ]

    window = sg.Window('ERROR', layout)

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Wróć':
            window.close()
            break