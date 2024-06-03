import os
if os.path.exists("nadawca/private.pem"):
    os.remove("nadawca/private.pem")
if os.path.exists("odbiorca/public.pem"):
    os.remove("odbiorca/public.pem")
if os.path.exists("odbiorca/sign.txt"):
    os.remove("odbiorca/sign.txt")
if os.path.exists("odbiorca/w_modified.png"):
    os.remove("odbiorca/w_modified.png")