# CSV Column Filter - Filtrowanie kolumn w plikach CSV

Prosty skrypt z interfacem graficznym do filtrowania kolumn w plikach CSV na podstawie fragmentu nazwy kolumny.

## Opis projektu

Ten skrypt został stworzony do pracy z dużymi plikami CSV zawierającymi dane z inklinometrów. Głównym celem jest możliwość szybkiego wyodrębnienia tylko tych kolumn, które zawierają określony fragment w nazwie (np. `_dA`, `_T`, `_dB`), przy zachowaniu:
- Pierwszej kolumny (zazwyczaj daty/czasy)
- Oryginalnej kolejności kolumn
- Oryginalnej struktury danych

## Funkcjonalności

- **Interfejs graficzny (GUI)** - Prosty interfejs w tkinter, nie wymaga znajomości linii poleceń
- **Automatyczne wykrywanie separatora** - Aktualnie ustawiony na średnik (`;`)
- **Zachowanie struktury** - Pierwsza kolumna (daty) jest zawsze zachowywana
- **Filtrowanie po fragmencie nazwy** - Możliwość wyboru kolumn zawierających określony fragment (np. `_dA`)
- **Filtrowanie po inklinometrze** - Dwie opcje:
  - Wybór konkretnego inklinometru (np. `Inkl_[1]`, `Ink_[6]`) → jeden plik
  - Automatyczne generowanie osobnych plików dla WSZYSTKICH inklinometrów
- **Filtrowanie po godzinie** - Dwie opcje:
  - Wszystkie dane (pełne wiersze)
  - Tylko wiersze z konkretną godziną (np. 18:00 każdego dnia)
- **Kombinacja filtrów** - Możliwość łączenia: fragment + inklinometr + godzina
- **Automatyczne wykrywanie inklinometrów** - Skrypt sam znajdzie wszystkie inklinometry w pliku
- **Kolumny MAX i MAX_COLUMN** - W trybie generowania osobnych plików, automatycznie dodawane są dwie kolumny:
  - `MAX` - maksymalna wartość z danego wiersza
  - `MAX_COLUMN` - nazwa kolumny, z której pochodzi wartość maksymalna
- **Podgląd logów** - Okno z informacjami o przetwarzaniu
- **Automatyczna nazwa wyjściowa** - Sugerowana nazwa pliku wyjściowego na podstawie wejściowego
- **Testowe pliki w osobnym folderze** - Wszystkie pliki wynikowe zapisywane do `test_outputs/`

## Struktura plików

```
inclinometers/
├── csv_column_filter.py      # Główny skrypt z GUI
├── test_filter.py             # Skrypt testowy (bez GUI)
├── testowe.csv                # Przykładowy plik danych
├── testowe_filtered_dA.csv    # Przykładowy plik wynikowy (_dA)
├── testowe_filtered_T.csv     # Przykładowy plik wynikowy (_T)
└── README.md                  # Dokumentacja
```

## Wymagania

- Python 3.6 lub nowszy
- Wbudowane biblioteki:
  - `tkinter` (interfejs graficzny)
  - `csv` (obsługa plików CSV)
  - `os` (operacje na plikach)

**Uwaga:** Wszystkie wymagane biblioteki są wbudowane w Python, nie ma potrzeby instalacji dodatkowych pakietów.

## Szybki start

**Nie potrzebujesz środowiska wirtualnego ani dodatkowych instalacji!**

```bash
# 1. Sprawdź Pythona
python3 --version

# 2. Uruchom skrypt
python3 csv_column_filter.py
```

**Szczegółowa instrukcja:** Zobacz [INSTALLATION.md](INSTALLATION.md)

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki
2. Upewnij się, że masz zainstalowany Python 3.6+

```bash
python3 --version
```

**Środowisko wirtualne:** NIE jest wymagane - używamy tylko wbudowanych bibliotek (`tkinter`, `csv`, `os`)

## Uruchomienie

### Metoda 1: Interfejs graficzny (GUI)

```bash
python3 csv_column_filter.py
```

### Metoda 2: Test z linii poleceń

```bash
python3 test_filter.py
```

## Jak używać

### Interfejs graficzny (csv_column_filter.py)

1. **Uruchom skrypt:**
   ```bash
   python3 csv_column_filter.py
   ```

2. **Wybierz plik wejściowy:**
   - Kliknij przycisk "Wybierz..." obok "Plik wejściowy"
   - Wybierz plik CSV do filtrowania

3. **Wpisz fragment nazwy kolumny:**
   - W polu "Fragment nazwy kolumny" wpisz fragment, który mają zawierać kolumny
   - Przykłady: `_dA`, `_T`, `_dB`, `_X`, `_Y`

4. **Opcjonalnie: wybierz tryb pracy z inklinometrami:**

   **Opcja A - Pojedynczy inklinometr (jeden plik):**
   - Zaznacz checkbox "Tylko z konkretnego inklinometru"
   - Wpisz nazwę inklinometru, np. `Inkl_[1]`, `Inkl_[2]`, `Ink_[5]`, `Ink_[6]`
   - Zostają tylko kolumny z tego inklinometru
   - Wynik: JEDEN plik z danymi wybranego inklinometru

   **Opcja B - Wszystkie inklinometry (wiele plików):**
   - Zaznacz checkbox "Generuj osobne pliki dla każdego inklinometru"
   - Wpisz nazwę bazową (np. `dane_12_00`)
   - Skrypt automatycznie wykryje wszystkie inklinometry
   - Wynik: WIELE plików, po jednym dla każdego inklinometru
     - `dane_12_00_Ink_5.csv`
     - `dane_12_00_Inkl_1.csv`
     - `dane_12_00_Inkl_2.csv`
     - itd.

5. **Wybierz opcję filtrowania wierszy:**
   - **Wszystkie dane** - zachowuje wszystkie wiersze z pliku
   - **Tylko wiersze z konkretną godziną** - wybierz tę opcję i wpisz godzinę w formacie HH:MM (np. 18:00)
     - Zostają tylko wiersze z podaną godziną z każdego dnia
     - Przydatne do wyciągnięcia dziennych pomiarów o tej samej porze

6. **Wybierz miejsce zapisu (opcjonalnie):**
   - Domyślnie nazwa jest generowana automatycznie (`plik_filtered.csv`)
   - Możesz ją zmienić klikając "Wybierz..." obok "Plik wyjściowy"

7. **Kliknij "Filtruj kolumny"**

8. **Sprawdź logi:**
   - W dolnej części okna zobaczysz szczegółowe informacje o procesie
   - Po zakończeniu pojawi się okno z potwierdzeniem

### Test z linii poleceń (test_filter.py)

Skrypt testowy przetwarza plik `testowe.csv` i tworzy dwa pliki wyjściowe:
- `testowe_filtered_dA.csv` - kolumny zawierające `_dA`
- `testowe_filtered_T.csv` - kolumny zawierające `_T`

```bash
python3 test_filter.py
```

## Przykłady użycia

### Przykład 1: Filtrowanie kolumn `_dA`

**Plik wejściowy:** `testowe.csv` (459 kolumn)

**Fragment:** `_dA`

**Wynik:** `testowe_filtered_dA.csv` (105 kolumn: 1 kolumna dat + 104 kolumny z `_dA`)

```
Date UTC;Ink_[5][0]_dA;Ink_[5][1]_dA;Ink_[5][2]_dA;...
25.09.2025 23:00;;;;...
25.09.2025 23:15;;;;...
```

### Przykład 2: Filtrowanie kolumn `_T`

**Plik wejściowy:** `testowe.csv` (459 kolumn)

**Fragment:** `_T`

**Wynik:** `testowe_filtered_T.csv` (104 kolumny: 1 kolumna dat + 103 kolumny z `_T`)

```
Date UTC;Ink_[5][1]_T;Ink_[5][2]_T;Ink_[5][3]_T;...
25.09.2025 23:00;;;;;...
25.09.2025 23:15;;;;;...
```

### Przykład 3: Filtrowanie kolumn `_dA` + tylko godzina 00:00

**Plik wejściowy:** `testowe.csv` (1342 wiersze, 459 kolumn)

**Fragment:** `_dA`

**Godzina:** `00:00`

**Wynik:** `testowe_00_00_dA.csv` (11 wierszy, 105 kolumn)

- Tylko wiersze z godziną 00:00 każdego dnia
- Z 1342 wierszy zostaje 11 (po jednym na dzień o północy)

```
Date UTC;Ink_[5][0]_dA;Ink_[5][1]_dA;Ink_[5][2]_dA;...
26.09.2025 00:00;;48.53;50.63;...
27.09.2025 00:00;31.78;48.62;50.73;...
28.09.2025 00:00;31.8;48.72;50.84;...
```

### Przykład 4: Filtrowanie kolumn `_T` + tylko godzina 18:00

**Plik wejściowy:** `testowe.csv` (1342 wiersze, 459 kolumn)

**Fragment:** `_T`

**Godzina:** `18:00`

**Wynik:** Tylko pomiary temperatury o 18:00 każdego dnia

- Przydatne do analizy dziennych wartości o tej samej porze
- Eliminuje fluktuacje godzinowe

### Przykład 5: Tylko inklinometr Inkl_[1], kolumny _dA

**Plik wejściowy:** `testowe.csv` (459 kolumn)

**Fragment:** `_dA`

**Inklinometr:** `Inkl_[1]`

**Wynik:** `test_Inkl1_dA.csv` (16 kolumn: 1 kolumna dat + 15 kolumn _dA z Inkl_[1])

- Wszystkie inklinometry: 104 kolumny _dA
- Tylko Inkl_[1]: 15 kolumn _dA

```
Date UTC;Inkl_[1][0]_dA;Inkl_[1][1]_dA;Inkl_[1][2]_dA;...
25.09.2025 23:00;1.96;10.05;8.13;19.51;...
25.09.2025 23:15;1.96;10.04;8.13;19.5;...
```

### Przykład 6: Inkl_[1] + _dA + godzina 00:00 (kombinacja wszystkich filtrów)

**Plik wejściowy:** `testowe.csv` (1342 wiersze, 459 kolumn)

**Fragment:** `_dA`

**Inklinometr:** `Inkl_[1]`

**Godzina:** `00:00`

**Wynik:** `test_Inkl1_dA_00_00.csv` (11 wierszy, 16 kolumn)

- Tylko inklinometr Inkl_[1]
- Tylko kolumny z _dA
- Tylko pomiary o północy każdego dnia
- Z 1342 wierszy → 11 wierszy

Idealny do analizy dziennych wartości jednego inklinometru o stałej porze!

### Przykład 7: Generowanie osobnych plików dla wszystkich inklinometrów

**Plik wejściowy:** `testowe.csv` (1342 wiersze, 459 kolumn, 8 inklinometrów)

**Fragment:** `_dA`

**Tryb:** Generuj osobne pliki

**Nazwa bazowa:** `pomiary_dA`

**Godzina:** `12:00`

**Wynik:** 8 osobnych plików, po jednym dla każdego inklinometru

```
pomiary_dA_Ink_5.csv     (11 wierszy, 16 kolumn)
pomiary_dA_Ink_6.csv     (11 wierszy, 15 kolumn)
pomiary_dA_Ink_7.csv     (11 wierszy, 14 kolumn)
pomiary_dA_Ink_8.csv     (11 wierszy, 9 kolumn)
pomiary_dA_Inkl_1.csv    (11 wierszy, 16 kolumn)
pomiary_dA_Inkl_2.csv    (11 wierszy, 16 kolumn)
pomiary_dA_Inkl_3.csv    (11 wierszy, 10 kolumn)
pomiary_dA_Inkl_4.csv    (11 wierszy, 16 kolumn)
```

**Przykładowa zawartość `pomiary_dA_Inkl_1.csv`:**
```
Date UTC;Inkl_[1][0]_dA;Inkl_[1][1]_dA;Inkl_[1][2]_dA;...;MAX;MAX_COLUMN
26.09.2025 12:00;1.97;10.08;8.15;19.53;...;19.53;Inkl_[1][3]_dA
27.09.2025 12:00;1.96;10.07;8.14;19.52;...;19.52;Inkl_[1][3]_dA
...
```

**Uwaga:** W trybie generowania osobnych plików, na końcu każdego pliku automatycznie dodawane są dwie kolumny:
- **MAX** - maksymalna wartość numeryczna z danego wiersza
- **MAX_COLUMN** - nazwa kolumny, w której znajduje się ta wartość maksymalna

**Zastosowania:**
- Automatyczne rozdzielenie danych na osobne pliki dla każdego urządzenia
- Łatwe porównanie wartości między inklinometrami (każdy w osobnym pliku)
- Przekazanie danych do innych osób/narzędzi (każdy bierze swój inklinometr)
- Redukcja rozmiaru plików - zamiast jednego dużego, wiele małych
- Jeden krok zamiast 8 ręcznych operacji!

## Struktura danych

### Format wejściowy

Skrypt oczekuje pliku CSV o następującej strukturze:

```
Date UTC;Kolumna1;Kolumna2_dA;Kolumna3_T;Kolumna4_dA;...
25.09.2025 23:00;wartość1;wartość2;wartość3;wartość4;...
25.09.2025 23:15;wartość1;wartość2;wartość3;wartość4;...
```

- **Separator:** średnik (`;`)
- **Pierwsza kolumna:** Daty/czasy (np. "Date UTC")
- **Pozostałe kolumny:** Dowolne nazwy z różnymi końcówkami

### Format wyjściowy

Plik wyjściowy zachowuje tę samą strukturę, ale zawiera tylko wybrane kolumny:

```
Date UTC;Kolumna2_dA;Kolumna4_dA;...
25.09.2025 23:00;wartość2;wartość4;...
25.09.2025 23:15;wartość2;wartość4;...
```

## Techniczne szczegóły

### Algorytm filtrowania

1. **Wczytanie pliku CSV** z użyciem modułu `csv`
2. **Identyfikacja nagłówków** (pierwszy wiersz)
3. **Filtrowanie kolumn:**
   - Zawsze zachowuje pierwszą kolumnę (indeks 0)
   - Przeszukuje pozostałe kolumny i wybiera te zawierające podany fragment
   - Zachowuje oryginalną kolejność kolumn
4. **Tworzenie nowego pliku:**
   - Zapisuje nagłówki wybranych kolumn
   - Dla każdego wiersza danych ekstraktuje wartości z wybranych kolumn
5. **Zapis do pliku** z użyciem tego samego separatora

### Obsługa błędów

Skrypt obsługuje następujące sytuacje:
- Brak pliku wejściowego
- Pusty plik CSV
- Brak pasujących kolumn
- Nieprawidłowy format pliku
- Błędy zapisu do pliku

## Rozszerzenia i modyfikacje

### Zmiana separatora

Aby zmienić separator z średnika na inny znak, zmodyfikuj następujące linie:

**W pliku `csv_column_filter.py`:**

```python
# Linia 123 (wczytywanie)
reader = csv.reader(f, delimiter=',')  # Zmień ';' na ','

# Linia 178 (zapisywanie)
writer = csv.writer(f, delimiter=',')  # Zmień ';' na ','
```

### Dodanie obsługi wielu fragmentów

Możesz rozszerzyć skrypt, aby akceptował wiele fragmentów naraz (np. `_dA,_T,_X`):

```python
filter_fragments = self.filter_text.get().split(',')
for i, col in enumerate(all_columns[1:], start=1):
    if any(fragment.strip() in col for fragment in filter_fragments):
        selected_indices.append(i)
        selected_columns.append(col)
```

### Dodanie możliwości wyboru pierwszej kolumny

Jeśli chcesz mieć możliwość wybrania, która kolumna ma być "kolumną dat":

```python
first_column_index = 0  # lub inna wartość
selected_indices = [first_column_index]
selected_columns = [all_columns[first_column_index]]
```

## Testowanie

### Testy jednostkowe

Plik `test_filter.py` zawiera podstawowe testy funkcjonalności:

```bash
python3 test_filter.py
```

Testy weryfikują:
- Wczytywanie pliku CSV
- Filtrowanie kolumn po fragmencie nazwy
- Zapis przefiltrowanych danych
- Zachowanie struktury i kolejności

### Testy manualne

1. Sprawdź czy GUI się uruchamia
2. Wybierz testowy plik CSV
3. Przetestuj różne fragmenty nazw kolumn
4. Sprawdź czy pliki wyjściowe są poprawne
5. Zweryfikuj liczby kolumn i wierszy

## FAQ - Najczęściej zadawane pytania

**Q: Czy mogę użyć skryptu z innym separatorem niż średnik?**

A: Tak, zobacz sekcję "Rozszerzenia i modyfikacje" - "Zmiana separatora"

**Q: Co się stanie jeśli nie ma kolumn zawierających podany fragment?**

A: Skrypt wyświetli ostrzeżenie i nie utworzy pliku wyjściowego

**Q: Czy pierwsza kolumna jest zawsze zachowywana?**

A: Tak, pierwsza kolumna (zazwyczaj daty) jest zawsze dołączana do wyniku

**Q: Czy mogę filtrować po wielu fragmentach naraz?**

A: Obecnie nie, ale możesz to łatwo dodać (zobacz "Rozszerzenia i modyfikacje")

**Q: Czy skrypt działa z dużymi plikami (>100MB)?**

A: Tak, skrypt wczytuje plik do pamięci, więc powinien działać z dużymi plikami jeśli masz wystarczająco dużo RAM

**Q: Czy mogę uruchomić skrypt bez GUI?**

A: Tak, użyj `test_filter.py` lub `test_time_filter.py` dla testów z linii poleceń

**Q: Jak działa filtrowanie po godzinie?**

A: Jeśli wybierzesz opcję "Tylko wiersze z konkretną godziną" i podasz np. "18:00", skrypt zachowa tylko te wiersze, gdzie w kolumnie z datą występuje godzina 18:00 (niezależnie od dnia)

**Q: Czy mogę wybrać wiele różnych godzin?**

A: Obecnie nie - możesz wybrać tylko jedną konkretną godzinę lub wszystkie dane. Jeśli potrzebujesz wielu godzin, uruchom skrypt kilka razy z różnymi godzinami

**Q: W jakim formacie podać godzinę?**

A: Format HH:MM, np. "18:00", "09:30", "23:45". Użyj dwóch cyfr dla godziny i minut

**Q: Jak nazywają się inklinometry w moim pliku?**

A: Otwórz plik CSV w edytorze i sprawdź nagłówki kolumn. Szukaj wzorców jak `Inkl_[1]`, `Inkl_[2]`, `Ink_[5]`, `Ink_[6]` itp. Nazwa inklinometru to część przed numerem czujnika w nawiasach kwadratowych

**Q: Czy mogę filtrować po wielu inklinometrach na raz?**

A: Obecnie nie - możesz wybrać tylko jeden inklinometr lub wszystkie. Jeśli potrzebujesz danych z kilku inklinometrów, uruchom skrypt kilka razy

**Q: Co się stanie jeśli podam błędną nazwę inklinometru?**

A: Skrypt nie znajdzie żadnych pasujących kolumn i wyświetli ostrzeżenie. Sprawdź pisownię - nazwa musi dokładnie odpowiadać początkowcom kolumn (np. `Inkl_[1]`, a nie `Inkl[1]`)

**Q: Gdzie zapisują się testowe pliki?**

A: Wszystkie pliki wynikowe z testów zapisują się do folderu `test_outputs/`, który jest ignorowany przez git

**Q: Jak działa opcja "Generuj osobne pliki dla każdego inklinometru"?**

A: Skrypt automatycznie wykrywa wszystkie inklinometry w pliku (np. Ink_[5], Inkl_[1] itd.) i dla każdego tworzy osobny plik CSV. Do nazwy bazowej dodawana jest nazwa inklinometru, np. `dane_12_00_Inkl_1.csv`

**Q: Ile plików zostanie utworzonych w trybie "generuj osobne pliki"?**

A: Tyle, ile inklinometrów ma kolumny z wybranym fragmentem. Np. dla `_dA` może być 8 plików (wszystkie inklinometry), ale dla `_dB` może być tylko 7 (jeśli jeden inklinometr nie ma kolumn _dB)

**Q: Gdzie zapisują się pliki w trybie "generuj osobne pliki"?**

A: W tym samym folderze co plik wejściowy. Jeśli plik wejściowy jest w `/home/user/dane/testowe.csv`, to pliki wyjściowe będą w `/home/user/dane/`

**Q: Czy mogę użyć obu opcji jednocześnie (pojedynczy inklinometr + generuj osobne pliki)?**

A: Nie - to wzajemnie wykluczające się opcje. Gdy zaznaczysz "Generuj osobne pliki", opcja pojedynczego inklinometru zostanie wyłączona

**Q: Jak nazywają się pliki wyjściowe w trybie "generuj osobne pliki"?**

A: Nazwa bazowa + `_` + nazwa inklinometru (z zamienionymi nawiasami na podkreślniki) + `.csv`. Przykład: `dane_12_00_Inkl_1.csv` dla inklinometru `Inkl_[1]`

**Q: Co to są kolumny MAX i MAX_COLUMN?**

A: W trybie generowania osobnych plików dla każdego inklinometru, na końcu pliku automatycznie dodawane są dwie kolumny:
- **MAX** - największa wartość numeryczna znaleziona w danym wierszu (pomijając kolumnę z datą)
- **MAX_COLUMN** - nazwa kolumny, z której pochodzi ta maksymalna wartość

Przykład: jeśli w wierszu wartości to `[1.97, 10.08, 8.15, 19.53]`, to MAX=19.53 a MAX_COLUMN wskaże trzecią kolumnę. To ułatwia szybką identyfikację najwyższych odczytów i ich źródeł.

**Q: Czy kolumny MAX i MAX_COLUMN pojawiają się zawsze?**

A: Nie - tylko w trybie "Generuj osobne pliki dla każdego inklinometru". W trybie pojedynczego pliku (bez split) te kolumny nie są dodawane.

**Q: Co się dzieje gdy w wierszu są tylko puste wartości lub tekst?**

A: Jeśli w wierszu nie ma żadnych wartości numerycznych, kolumny MAX i MAX_COLUMN będą puste. Skrypt pomija wartości nie-numeryczne i błędne podczas szukania maksimum.

## Licencja

Ten projekt jest dostępny na licencji MIT.

## Autor

Projekt stworzony do pracy z danymi z inklinometrów.

## Kontakt

W przypadku pytań lub problemów, zgłoś issue w repozytorium projektu.

---

**Wersja:** 1.0
**Data:** 2025-11-07
**Python:** 3.6+
