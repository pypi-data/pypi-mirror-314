# latest-indonesia-earthquake
this package will get the latest earthquake from BMKG -Meteorology, Climatology, and Geophysics Agency

## HOW IT WORKS ?

This package uses beautifllsoup4 and a request which will produce a jSON file output that is ready to be used for web 
or mobile applications



## HOW to use?

1. make file main.py
2. paste this code to file main.py

import gempaterkini

from gempaterkini.gempaUPDATE.__init__ import bencana, gempaTerkini


## aplikasi gempaterkini folder utama (pembuatan secara prosedural)
if __name__ == '__main__':
    result = gempaterkini.exstrasi_data()
    gempaterkini.tampilkan_data(result)


## aplikasi gempaUPDATE subfolder (pembuatan secara OOP)
if __name__ == '__main__':
    gempa_indonesia = gempaTerkini("https://bmkg.go.id")
    print(f'Aplikasi Utama menggunakan package yang memiliki deskripsi {gempa_indonesia.description}')
    gempa_indonesia.tampilkan_keterangan()
    gempa_indonesia.run()

3. run program



enjoyy the programm

