import PySimpleGUI as sg
import os
import functions.error as error
import nadawca.szyfrowanie as sz
import odbiorca.odszyfrowanie as odsz
import functions.clear as clear
import functions.RSA as RSA
import functions.file_select as select

filename='none'

layout = [
    [sg.Text("Co chcesz zrobić?")],
    [sg.Button('Generowanie kluczy RSA')],
    [sg.Button('Szyfrowanie pliku')],
    [sg.Button('Odszyfrowanie pliku')],
    [sg.Button('Usuń pliki')]
]

window = sg.Window('RSA', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == 'Generowanie kluczy RSA':
        RSA.main(select.main())
    if event == 'Szyfrowanie pliku':
        if os.path.exists("nadawca/private.key"):
            filename = sz.main(select.main())
        else:
            error.main('code')
    if event == 'Odszyfrowanie pliku':
        if os.path.exists("odbiorca/public.key"):
            odsz.main(filename)
        else:
            error.main('decode')
    if event == 'Usuń pliki':
        clear.main(filename)