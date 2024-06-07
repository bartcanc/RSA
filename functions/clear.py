import os
import functions.error as err
def main(filename):
    # if(filename == 'none'):
    #     err.main('none')
    #     return
    if os.path.exists("nadawca/private.key"):
        os.remove("nadawca/private.key")
    if os.path.exists("odbiorca/public.key"):
        os.remove("odbiorca/public.key")
    if os.path.exists("odbiorca/sign.txt"):
        os.remove("odbiorca/sign.txt")
    if os.path.exists(filename):
        os.remove(filename)