# Instrukcja instalacji i uruchomienia

## Krótka odpowiedź

**Czy potrzebuję środowiska wirtualnego?**

**NIE** - Skrypt używa tylko wbudowanych bibliotek Pythona (`tkinter`, `csv`, `os`), więc:
- Nie musisz tworzyć środowiska wirtualnego
- Nie musisz instalować żadnych dodatkowych pakietów (pip install)
- Wystarczy Python 3.6+ zainstalowany w systemie

## Wymagania systemowe

### Python

Upewnij się, że masz zainstalowany Python 3.6 lub nowszy:

```bash
python3 --version
```

Powinieneś zobaczyć coś w rodzaju:
```
Python 3.12.3
```

### tkinter (interfejs graficzny)

Na większości systemów `tkinter` jest już zainstalowany z Pythonem. Sprawdź:

```bash
python3 -c "import tkinter; print('tkinter OK')"
```

Jeśli zobaczysz błąd, zainstaluj tkinter:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
# tkinter jest już wbudowany w Python na macOS
# Jeśli nie działa, przeinstaluj Python z oficjalnej strony:
# https://www.python.org/downloads/macos/
```

**Windows:**
```
tkinter jest automatycznie instalowany z oficjalnym instalatorem Pythona
```

## Instalacja krok po kroku

### Opcja 1: Klonowanie z GitHub (gdy repozytorium jest już utworzone)

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/TWOJA_NAZWA/inclinometers.git

# 2. Wejdź do katalogu
cd inclinometers

# 3. Uruchom skrypt
python3 csv_column_filter.py
```

### Opcja 2: Pobranie plików ręcznie

```bash
# 1. Utwórz katalog projektu
mkdir csv-column-filter
cd csv-column-filter

# 2. Pobierz pliki z GitHub (ręcznie lub wget):
# - csv_column_filter.py
# - test_filter.py
# - README.md
# - TECHNICAL_DOCS.md

# 3. Uruchom skrypt
python3 csv_column_filter.py
```

## Uruchomienie

### Metoda 1: Interfejs graficzny (GUI)

```bash
# Uruchom skrypt z GUI
python3 csv_column_filter.py
```

To otworzy okno interfejsu graficznego gdzie możesz:
1. Wybrać plik wejściowy
2. Podać fragment nazwy kolumny
3. Wybrać plik wyjściowy
4. Kliknąć "Filtruj kolumny"

### Metoda 2: Test z linii poleceń (bez GUI)

```bash
# Uruchom testy
python3 test_filter.py
```

To przetworzy plik `testowe.csv` i utworzy:
- `testowe_filtered_dA.csv` (kolumny z `_dA`)
- `testowe_filtered_T.csv` (kolumny z `_T`)

### Metoda 3: Zrobić skrypt wykonywalnym (Linux/macOS)

```bash
# Nadaj uprawnienia wykonywania
chmod +x csv_column_filter.py

# Uruchom bezpośrednio
./csv_column_filter.py
```

## Środowisko wirtualne (opcjonalne)

Choć **nie jest wymagane**, możesz używać środowiska wirtualnego jeśli:
- Chcesz izolować projekt
- Planujesz dodać zewnętrzne biblioteki w przyszłości (np. pandas)
- Pracujesz nad wieloma projektami Pythona

### Tworzenie środowiska wirtualnego

```bash
# 1. Utwórz środowisko wirtualne
python3 -m venv venv

# 2. Aktywuj środowisko
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 3. (Opcjonalnie) Zainstaluj dodatkowe pakiety
# pip install pandas  # jeśli chcesz używać pandas

# 4. Uruchom skrypt
python csv_column_filter.py

# 5. Dezaktywuj środowisko (gdy skończysz)
deactivate
```

### .gitignore dla środowiska wirtualnego

Jeśli używasz środowiska wirtualnego, dodaj do `.gitignore`:

```
venv/
__pycache__/
*.pyc
*.pyo
*.csv  # opcjonalnie - jeśli nie chcesz commitować plików CSV
```

## Testowanie instalacji

### Test 1: Sprawdź wersję Pythona

```bash
python3 --version
```

Oczekiwany wynik: `Python 3.6.x` lub nowszy

### Test 2: Sprawdź tkinter

```bash
python3 -c "import tkinter; print('tkinter OK')"
```

Oczekiwany wynik: `tkinter OK`

### Test 3: Sprawdź składnię skryptu

```bash
python3 -m py_compile csv_column_filter.py
```

Oczekiwany wynik: Brak błędów (nie wyświetli nic)

### Test 4: Uruchom testy funkcjonalne

```bash
python3 test_filter.py
```

Oczekiwany wynik:
```
============================================================
TEST: Filtrowanie kolumn zawierających '_dA'
============================================================
Wczytano 1342 wierszy i 459 kolumn
...
✓ Sukces! Zapisano 1342 wierszy i 105 kolumn
```

### Test 5: Uruchom GUI

```bash
python3 csv_column_filter.py
```

Oczekiwany wynik: Otworzy się okno aplikacji

## Rozwiązywanie problemów

### Problem: `ModuleNotFoundError: No module named 'tkinter'`

**Rozwiązanie:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

### Problem: `Permission denied` przy uruchamianiu

**Rozwiązanie:**
```bash
# Dodaj uprawnienia wykonywania
chmod +x csv_column_filter.py

# Lub uruchom przez interpreter
python3 csv_column_filter.py
```

### Problem: GUI nie otwiera się w WSL

**Wyjaśnienie:** WSL (Windows Subsystem for Linux) wymaga serwera X11 do wyświetlania GUI.

**Rozwiązanie:**

1. Zainstaluj X Server na Windows:
   - [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
   - [Xming](http://www.straightrunning.com/XmingNotes/)

2. Uruchom X Server

3. W WSL ustaw zmienną DISPLAY:
   ```bash
   export DISPLAY=:0
   ```

4. Lub użyj wersji testowej bez GUI:
   ```bash
   python3 test_filter.py
   ```

### Problem: `UnicodeDecodeError` przy czytaniu CSV

**Rozwiązanie:**

Twój plik CSV może mieć inne kodowanie. Zmień w skrypcie:

```python
# Zamiast:
with open(self.input_file.get(), 'r', encoding='utf-8') as f:

# Spróbuj:
with open(self.input_file.get(), 'r', encoding='latin-1') as f:
# lub
with open(self.input_file.get(), 'r', encoding='cp1252') as f:
```

### Problem: Błąd separatora (niepoprawne kolumny)

**Wyjaśnienie:** Twój CSV używa innego separatora niż średnik (`;`)

**Rozwiązanie:**

Sprawdź separator w pliku:
```bash
head -n 1 twoj_plik.csv
```

Jeśli używa przecinka (`,`), zmień w skrypcie:

```python
# Linia 123:
reader = csv.reader(f, delimiter=',')  # Zmień ';' na ','

# Linia 178:
writer = csv.writer(f, delimiter=',')  # Zmień ';' na ','
```

## Struktura katalogów

Po instalacji powinieneś mieć:

```
inclinometers/
├── csv_column_filter.py         # Główny skrypt z GUI
├── test_filter.py                # Skrypt testowy
├── testowe.csv                   # Przykładowy plik danych
├── README.md                     # Dokumentacja użytkownika
├── TECHNICAL_DOCS.md             # Dokumentacja techniczna
├── INSTALLATION.md               # Ten plik
└── (opcjonalnie) venv/           # Środowisko wirtualne
```

## Quick Start (dla niecierpliwych)

```bash
# Sprawdź Pythona
python3 --version

# Sprawdź tkinter
python3 -c "import tkinter"

# Uruchom
python3 csv_column_filter.py
```

To wszystko! Nie potrzebujesz nic więcej.

## Aktualizacja

Jeśli repozytorium zostało zaktualizowane:

```bash
# Pobierz najnowsze zmiany
git pull origin main

# Uruchom ponownie
python3 csv_column_filter.py
```

## Wsparcie

W przypadku problemów:

1. Sprawdź sekcję "Rozwiązywanie problemów" powyżej
2. Sprawdź FAQ w README.md
3. Zgłoś issue na GitHubie

---

**Wersja:** 1.0
**Data:** 2025-11-07
**Testowane na:**
- Ubuntu 20.04+ (Python 3.8+)
- macOS 11+ (Python 3.9+)
- Windows 10+ (Python 3.8+)
- WSL2 Ubuntu (Python 3.8+)
