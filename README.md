
# Podpis cyfrowy

Prosty podpis cyfrowy i weryfikacja zrealizowana w języku Python. 

**Wykorzystuje generator liczb losowych oparty na artykule:** 

https://www.researchgate.net/publication/258391920_Random_Numbers_Generated_from_Audio_and_Video_Sources

**Generator liczb losowych:**

https://github.com/bartcanc/Random-Numbers-Generated-from-Audio-and-Video-Sources-Implementation-in-Python-

## Opis wykorzystywanych funkcji
* **RSA.py**
```
def import_file(filename):                               // funkcja odczytująca plik z podanej ścieżki
    with open(filename, 'rb') as file:
        imported = file.read()
    return imported                                      // zwraca dane odczytane z pliku

def main(file):
    imported_data = import_file(file)
    index=0

    def random_from_file(n):                             // funkcja implementująca generator liczb losowych
        nonlocal imported_data, index
        end_index = index + n
        if end_index > len(imported_data):               // w przypadku, gdy z pliku zostało zczytanych za mało liczb 
            add_data = os.urandom(len(imported_data))    // generowane są dodatkowe liczby losowe
            imported_data += add_data
        result = imported_data[index:end_index]
        index += n
        return result                                    // zwracana jest żądana ilość bitów

    key = RSA.generate(2048, e=65537, randfunc=random_from_file)    // generowanie kluczy RSA za pomocą funkcji z biblioteki PyCryptoDome

    private = key.export_key()                           // ekstrakcja klucza prywatnego i publicznego
    public = key.public_key().export_key()

    with open('nadawca/private.key', 'wb') as pv:        // wysłanie klucza prywatnego do nadawcy
        pv.write(private)
    with open('odbiorca/public.key', 'wb') as pub:       // wysłanie klucza publicznego do odbiorcy
        pub.write(public)
```
  
* **clear.py**
```
def main(filename):        
    # if(filename == 'none'):
    #     err.main('none')
    #     return
    if os.path.exists("nadawca/private.key"):    // zabezpieczenie przed usuwaniem pliku który nie istnieje
        os.remove("nadawca/private.key")         // usunięcie pliku
    if os.path.exists("odbiorca/public.key"):
        os.remove("odbiorca/public.key")
    if os.path.exists("odbiorca/sign.txt"):
        os.remove("odbiorca/sign.txt")
    if os.path.exists(filename):
        os.remove(filename)
```
* **error.py**
```
def main(message):                      // argumentem wejściowym jest ciąg znaków oznaczający typ błędu
    if message == 'code':               // 'code' - przypadek, gdy użytkownik chce zaszyfrować plik,
        layout = [                      // ale bez wygenerowanych najpierw kluczy RSA
            [sg.Text("Najpierw wygeneruj klucze RSA!")],
            [sg.Button('Wróć')]
        ]
    elif message == 'decode':           // 'decode' - przypadek, gdy użytkownik chce rozszyfrować
        layout = [                      // plik, który nie został zaszyfrowany
            [sg.Text("Najpierw zaszyfruj plik!")],
            [sg.Button('Wróć')]
        ]
    elif message == 'none':             // 'none' - przypadek, gdy użytkownik chce usunąć pliki,
        layout = [                      // których nie ma
            [sg.Text("Brak plików do usunięcia.")],
            [sg.Button('Wróć')]
        ]

    window = sg.Window('ERROR', layout)

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Wróć':
            window.close()
            break
```
* **file_select.py**
```
def main(event):                          // Argumentem wejściowym jest zdarzenie zdefiniowane
    layout = [                            // w głównej funkcji
        [sg.I(), sg.FileBrowse()],
        [sg.Ok(), sg.Cancel()]
    ]

    if event == 'Generowanie kluczy RSA':                             // W zależności od zdarzenia wejściowego ustawiana 
        window = sg.Window("Wybierz plik z losowymi bitami", layout)  // jest odpowiednia nazwa okna
    elif event == 'Szyfrowanie pliku':
        window = sg.Window("Wybierz plik do zaszyfrowania", layout)
    event, values = window.read()
    if event == 'Cancel':
        window.close()
    window.close()
    return values[0]
```
* **szyfrowanie.py**
```  
def main(filename):                                // Argumentem wejściowym jest ścieżka do pliku
    with open(filename, "rb") as f:                // który użytkownik chce zaszyfrować
        file = f.read()
    with open('nadawca/private.key', "rb") as f:   // z pliku odczytywany jest klucz prywatny
        privateKey = RSA.import_key(f.read())
    sha = SHA.new()
    sha.update(file)
    podpis = PKCS.new(privateKey).sign(sha)        // tworzenie podpisu
    with open('odbiorca/sign.txt', "w") as file:   // wysłanie podpisu do odbiorcy
        file.write(podpis.hex())
    with open(filename, "rb") as f:
        with open('odbiorca/'+os.path.basename(filename), "wb") as output:    // wysłanie zahaszowanego pliku do odbiorcy
            output.write(f.read())
    return 'odbiorca/'+os.path.basename(filename)  // zwracana jest ścieżka do zahaszowanego pliku
```
* **odszyfrowanie.py**
```
def main(filename):                                // Argumentem wejściowym jest ścieżka do pliku
    with open(filename, "rb") as f:                // który użytkownik chce rozszyfrować
        file = f.read()
    with open('odbiorca/sign.txt') as f:           // odczytanie podpisu z pliku
        podpis = f.read()
    sha = SHA.new()
    sha.update(file)
    podpis = bytes.fromhex(podpis)                 // konwersja podpisu na bajty
    with open("odbiorca/public.key") as f:         // odczytanie klucza publicznego z pliku
        publicKey = RSA.importKey(f.read())
    ver = PKCS.new(publicKey).verify(sha,podpis)   // weryfikacja podpisu cyfrowego za pomocą funkcji 
                                                   // z biblioteki PyCryptoDome
    if ver:                                        
        layout = [ [sg.Text("Message verified!")],   // w przypadku pomyślnej weryfikacji   
            [sg.Button('Close')]]                    // wyświetlana jest wiadomość potwierdzająca
    else:
        layout = [ [sg.Text("ERROR: Message modified!")],  // w przeciwnym wypadku, wyświetlany jest
            [sg.Button('Close')]]                          // błąd

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
```

## Interfejs graficzny
<div align="center">
	<img src="/readme_images/main.png">
  
  Po włączeniu programu, wyświetlane jest okno z czterema opcjami.

  <img src="/readme_images/decode error.png">
  <img src="/readme_images/code error.png">

  W przypadku wybrania opcji szyfrowania/odszyfrowania pliku bez uprzedniego wygenerowania kluczy RSA/zakodowania pliku, wyświetlony zostanie odpowiedni błąd.
</div>

* **Generowanie kluczy RSA**
  <div align="center">
	<img src="/readme_images/keygen1.png">
  
  Po wybraniu tej opcji, wyświetlane jest okno, z poziomu którego użytkownik musi wybrac plik z ciągiem bitowym potrzebny do wygenerowania kluczy RSA.


  <img src="/readme_images/keygen2.png">

  Po wybraniu pliku, należy kliknąć 'Ok'.


  <img src="/readme_images/keygen result.png">

  Klucze zostały wygenerowane i wysłane do odpowiednich osób (klucz prywatny do nadawcy, klucz publiczny do odbiorcy).
</div>

* **Szyfrowanie pliku**
<div align="center">
	<img src="/readme_images/code1.png">
  
  Podobnie jak w opcji 'Generowanie kluczy RSA', należy wybrać plik.

  <img src="/readme_images/code2.png">

  Jako przykład został wybrany plik w formacie PNG.

  <img src="/readme_images/code result.png">

  Podpis cyfrowy i zahaszowany plik został wysłany do odbiorcy.

</div>

* **Odszyfrowanie pliku**
<div align="center">
	<img src="/readme_images/decode result.png">
  
  Po wygenerowaniu kluczy i zakodowaniu pliku, sprawdzamy podpis cyfrowy (tutaj został sprawdzony pomyślnie).

  <img src="/readme_images/key edit.png">
  
  <img src="/readme_images/key edit result.png">
    
  W przypadku zmiany np. klucza publicznego, program wyświetla komunikat odnośnie błędu weryfikacji podpisu cyfrowego.

</div>
