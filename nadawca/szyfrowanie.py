from Crypto.Hash import SHA256 as SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS
from Crypto.PublicKey import RSA

with open('nadawca/w.png', "rb") as f:
    file = f.read()
with open('nadawca/private.pem', "rb") as f:
    privateKey = RSA.import_key(f.read())
sha = SHA.new()
sha.update(file)
podpis = PKCS.new(privateKey).sign(sha)
with open('odbiorca/sign.txt', "w") as file:     
    file.write(podpis.hex())
with open('nadawca/w.png', "rb") as f:
    with open('odbiorca/w_modified.png', "wb") as output:
        output.write(f.read())