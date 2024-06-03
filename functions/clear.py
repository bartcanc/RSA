import os
def main(filename='testfolder/hej'):
    if os.path.exists("nadawca/private.key"):
        os.remove("nadawca/private.key")
    if os.path.exists("odbiorca/public.key"):
        os.remove("odbiorca/public.key")
    if os.path.exists("odbiorca/sign.txt"):
        os.remove("odbiorca/sign.txt")
    if os.path.exists(filename):
        os.remove(filename)