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
- **Podgląd logów** - Okno z informacjami o przetwarzaniu
- **Automatyczna nazwa wyjściowa** - Sugerowana nazwa pliku wyjściowego na podstawie wejściowego

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

4. **Wybierz miejsce zapisu (opcjonalnie):**
   - Domyślnie nazwa jest generowana automatycznie (`plik_filtered.csv`)
   - Możesz ją zmienić klikając "Wybierz..." obok "Plik wyjściowy"

5. **Kliknij "Filtruj kolumny"**

6. **Sprawdź logi:**
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

A: Tak, użyj `test_filter.py` lub zmodyfikuj funkcję `filter_columns` do użycia z linii poleceń

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
