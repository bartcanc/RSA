from Crypto.Hash import SHA256 as SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS
from Crypto.PublicKey import RSA
import PySimpleGUI as sg

with open('odbiorca/w_modified.png', "rb") as f:
    file = f.read()
with open('odbiorca/sign.txt') as f:
    podpis = f.read()
sha = SHA.new()
sha.update(file)
podpis = bytes.fromhex(podpis)
with open("odbiorca/public.pem") as f:
    publicKey = RSA.importKey(f.read())
ver = PKCS.new(publicKey).verify(sha,podpis)

if ver:
    layout = [ [sg.Text("Message verified!")],
          [sg.Button('Close')]]
else:
    layout = [ [sg.Text("ERROR: Message modified!")],
          [sg.Button('Close')]]

window = sg.Window('Result', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        break

window.close()
# if ver:
#     print("Message verified!")
# else:
#     print("Message modified!")