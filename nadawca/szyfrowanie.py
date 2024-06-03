from Crypto.Hash import SHA256 as SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS
from Crypto.PublicKey import RSA
import os

def main(filename):
    with open(filename, "rb") as f:
        file = f.read()
    with open('nadawca/private.key', "rb") as f:
        privateKey = RSA.import_key(f.read())
    sha = SHA.new()
    sha.update(file)
    podpis = PKCS.new(privateKey).sign(sha)
    with open('odbiorca/sign.txt', "w") as file:     
        file.write(podpis.hex())
    with open(filename, "rb") as f:
        with open('odbiorca/'+os.path.basename(filename), "wb") as output:
            output.write(f.read())
    return 'odbiorca/'+os.path.basename(filename)