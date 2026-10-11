# Landsat 8: wykład i laboratorium

Projekt analizy danych Landsat 8 i generowania interaktywnej mapy internetowej. Wersja V3.

## Materiały

- [Notatnik Jupyter](notebooks/landsat_do_www_v3.ipynb) — wykonany, z wynikami, objaśnieniami i pełnymi poleceniami SSH/SCP.
- [Polecenia iTerm](docs/polecenia_iterm.md) — środowisko, uruchomienie, podgląd i publikacja.
- [Kod Pythona](src/landsat_lab.py) — wspólna implementacja używana przez notatnik i konsolę.
- [Wyniki](outputs/summary.json) — statystyki i parametry obliczeń.

## Szybki start

Polecenia z katalogu `LABOLATORIUM`. Przygotuj Python **3.12**, paczkę danych i dostęp do konta AGH **przed zajęciami**.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m ipykernel install --sys-prefix --name landsat-lab --display-name "Python (Landsat LAB)"
python -m jupyterlab notebooks/landsat_do_www_v3.ipynb
```

Wybierz kernel `Python (Landsat LAB)`. Notatnik wykonuje się od początku bez ręcznego przygotowania plików w QGIS. Publikacja jest osobnym krokiem wykonywanym w terminalu przez właściciela konta.

Uruchomienie bez notatnika:

```bash
python src/landsat_lab.py
python -m http.server 8000 --bind 127.0.0.1 --directory outputs/site
```

Otwórz `http://127.0.0.1:8000/`. Serwer zatrzymasz przez Ctrl+C. Do podglądu gotowej strony wystarczy Python ze standardowym modułem http.server; przeliczanie nie jest wymagane.

## Co powstaje

- `outputs/rasters/`: NDVI, NDBI, MNDWI w float32 oraz rastry prezentacyjne RGBA.
- `outputs/figures/`: ilustracje wyników.
- `outputs/site/`: gotowa strona, lokalny Leaflet, geometria granicy i 512 kafelków XYZ.
- `outputs/summary.json`: raport, m.in. liczby pikseli, średnie i wartości spoza [-1,1].

Strona pozwala wybrać NDVI/NDBI/MNDWI/RGB, zmienić przezroczystość i wrócić do całego obszaru. Kafelki powstają dla zoomów 9–12. Dalsze powiększenie nie zwiększa rozdzielczości źródła. Podkład OpenStreetMap wymaga internetu; warstwy własne oraz Leaflet są lokalne.

## Dane i istotne założenia

Scena: `LC08_L1TP_188025_20130807_20170503_01_T1`, USGS/EROS, 2013-08-07, Collection 1 Surface Reflectance. Dostarczono prostokątny wycinek 1583 × 1982 o rozdzielczości 30 m, kanały B2–B6 i dwie warstwy QA. Paczka wejściowa ma około 23 MB. Nie trzeba pobierać pełnej sceny.

Granica pochodzi z oryginalnego projektu. Brak PRJ i DBF w źródłowym SHP wymagał odtworzenia CRS: przyjęto EPSG:32634 na podstawie zgodności ze znajdującymi się w projekcie przyciętymi rastrami. GeoJSON zapisano w EPSG:4326. Szczegóły i sumy kontrolne rastrów są w [manifest.json](data/manifest.json). To granica ćwiczeniowa, bez nowej weryfikacji urzędowego przebiegu.

Kod czyta skalę i zakresy DN z XML. Zachowuje poprawne zera i wartości ujemne, maskuje NoData, chmury, cień, śnieg, wysoką pewność chmur/cirrus, przesłonięcie terenu i nasycenie B2–B6. Woda pozostaje ważna. Wspólna maska obejmuje 1 729 266 ważnych pikseli. Obsługiwany jest dostarczony produkt C1; C2 wymaga osobnego adaptera skalowania i QA.

Wskaźnik `(B3-B6)/(B3+B6)` nosi poprawioną nazwę **MNDWI** (w starym kodzie `ndwi`). Wyniki numeryczne nie są obcinane do [-1,1]; tylko skala kolorów ma taki zakres. Wartości spoza zakresu są raportowane.

Wszystkie obliczenia i eksport wykonuje Python. Rasterio korzysta z GDAL jako biblioteki. Kod nie uruchamia QGIS ani narzędzi gdalwarp/gdal_translate/gdal2tiles w powłoce. HTML/JavaScript służy wyłącznie wyświetlaniu gotowych warstw.

## Publikacja na AGH

Pełna procedura znajduje się w [instrukcji iTerm](docs/polecenia_iterm.md) oraz notatniku. Korzystamy z nowego podkatalogu `public_html/landsat-DATA-GODZINA`, aby nie zastępować istniejącej strony głównej.

Dokumentacja [CRI AGH](https://cri.agh.edu.pl/uslugi/konta-unix) wymaga sieci AGH lub VPN. Studenci używają hosta SSH `student.agh.edu.pl`, prowadzący `galaxy.agh.edu.pl`. Strony studentów są dostępne w sieci uczelni/VPN. Pakiet nie zawiera haseł i nie publikuje samoczynnie. Rzeczywistego przesyłania na konto AGH nie wykonano.

Wskazana pierwotna strona home.agh.edu.pl/~owerko nie była dostępna podczas przygotowania. Odtworzono funkcję mapy warstwowej na podstawie kodu projektu, bez deklarowania zgodności jej wyglądu 1:1.

## Kontrola i odtwarzalność

```bash
python -m unittest discover -s tests
```

Sprawdzono: pięć testów istotnych dla obliczeń, pełne wykonanie notatnika z czystego kernela, odczyt kontrolny GeoTIFF oraz cztery warstwy mapy w izolowanej przeglądarce. Zdalne SSH/SCP wymaga sprawdzenia z własnym kontem.

`requirements.txt` utrwala bezpośrednie zależności dla studenta. `requirements-lock.txt` jest pełnym zapisem środowiska sprawdzającego (w tym biblioteki do tworzenia PDF). Dla odtworzenia pełnego środowiska użyj `python -m pip install -r requirements-lock.txt`; plik zawiera macOS-owe appnope, więc dla innych systemów preferuj requirements.txt.

## Autorstwo i licencje

Materiały źródłowe: S. Moliński. Licencja projektu: [LICENSE](LICENSE). Leaflet: [licencja biblioteki](src/vendor/LICENSE-Leaflet.txt).
