from Crypto.PublicKey import RSA
import os

def import_file(filename):
    with open(filename, 'rb') as file:
        imported = file.read()
    return imported

imported_data = import_file('random_bit_for_key.txt')
index=0

def random_from_file(n):
    global imported_data, index
    end_index = index + n
    if end_index > len(imported_data):
        add_data = os.urandom(len(imported_data))
        imported_data += add_data
    result = imported_data[index:end_index]
    index += n
    return result

key = RSA.generate(2048, e=65537, randfunc=random_from_file)

private = key.export_key()
public = key.public_key().export_key()

with open('private.pem', 'wb') as pv:
    pv.write(private)
with open('public.pem', 'wb') as pub:
    pub.write(public)