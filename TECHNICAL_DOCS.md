# Dokumentacja Techniczna - CSV Column Filter

## Architektura aplikacji

### Struktura kodu

```
csv_column_filter.py
├── Importy (csv, tkinter, os)
├── Klasa CSVColumnFilterApp
│   ├── __init__() - Inicjalizacja GUI
│   ├── create_widgets() - Tworzenie interfejsu
│   ├── log() - Logowanie wiadomości
│   ├── select_input_file() - Dialog wyboru pliku wejściowego
│   ├── select_output_file() - Dialog wyboru pliku wyjściowego
│   └── filter_columns() - Główna logika filtrowania
└── main() - Uruchomienie aplikacji
```

## Szczegółowy opis funkcji

### `__init__(self, root)`

**Opis:** Konstruktor klasy, inicjalizuje zmienne i tworzy interfejs

**Parametry:**
- `root` (tk.Tk) - Główne okno aplikacji

**Zmienne instancji:**
- `self.root` - Referencja do głównego okna
- `self.input_file` (StringVar) - Ścieżka do pliku wejściowego
- `self.output_file` (StringVar) - Ścieżka do pliku wyjściowego
- `self.filter_text` (StringVar) - Fragment nazwy kolumny (domyślnie "_dA")
- `self.time_filter_mode` (StringVar) - Tryb filtrowania: "all" lub "specific_time"
- `self.specific_time` (StringVar) - Konkretna godzina do filtrowania (domyślnie "18:00")

**Wywołania:**
- `self.create_widgets()` - Tworzy wszystkie elementy GUI

---

### `create_widgets(self)`

**Opis:** Tworzy wszystkie elementy interfejsu graficznego

**Struktura GUI:**

```
┌─────────────────────────────────────────────┐
│ [Label] Plik wejściowy:                     │
│ [Entry: input_file]        [Button: Wybierz]│
├─────────────────────────────────────────────┤
│ [Label] Fragment nazwy:                     │
│ [Entry: filter_text]  [Label: (np. _dA)]   │
├─────────────────────────────────────────────┤
│ [Label] Filtrowanie wierszy:                │
│   ○ Wszystkie dane (pełne wiersze)          │
│   ○ Tylko wiersze z konkretną godziną:      │
│     [Entry: specific_time] (format HH:MM)   │
├─────────────────────────────────────────────┤
│ [Label] Plik wyjściowy:                     │
│ [Entry: output_file]       [Button: Wybierz]│
├─────────────────────────────────────────────┤
│           [Button: Filtruj kolumny]          │
├─────────────────────────────────────────────┤
│ [Label] Logi:                               │
│ [ScrolledText: log_text]                    │
│ (obszar przewijany dla logów)               │
└─────────────────────────────────────────────┘
```

**Elementy:**
- 3 ramki (Frame) dla grup kontrolek
- 2 przyciski wyboru plików (filedialog)
- 1 główny przycisk "Filtruj kolumny"
- 1 przewijane pole tekstowe dla logów

---

### `log(self, message)`

**Opis:** Dodaje wiadomość do okna logów

**Parametry:**
- `message` (str) - Wiadomość do wyświetlenia

**Działanie:**
1. Dodaje wiadomość na końcu pola tekstowego
2. Przewija do końca (see(END))
3. Aktualizuje GUI (root.update())

**Przykład użycia:**
```python
self.log("Rozpoczynam przetwarzanie...")
self.log(f"Znaleziono {count} kolumn")
```

---

### `select_input_file(self)`

**Opis:** Otwiera dialog wyboru pliku wejściowego

**Działanie:**
1. Wyświetla dialog wyboru pliku (filedialog.askopenfilename)
2. Ustawia wybraną ścieżkę w `self.input_file`
3. Automatycznie generuje nazwę pliku wyjściowego jeśli nie została ustawiona

**Przykładowa automatyczna nazwa:**
- Input: `/path/to/testowe.csv`
- Output: `/path/to/testowe_filtered.csv`

---

### `select_output_file(self)`

**Opis:** Otwiera dialog wyboru lokalizacji zapisu

**Działanie:**
1. Wyświetla dialog zapisu pliku (filedialog.asksaveasfilename)
2. Domyślne rozszerzenie: `.csv`
3. Ustawia wybraną ścieżkę w `self.output_file`

---

### `toggle_time_input(self)`

**Opis:** Włącza/wyłącza pole wprowadzania godziny w zależności od wyboru radio button

**Działanie:**
- Jeśli `time_filter_mode == "specific_time"` → włącz pole (state='normal')
- Jeśli `time_filter_mode == "all"` → wyłącz pole (state='disabled')

**Wywołanie:** Automatyczne przy zmianie radio button (command callback)

---

### `filter_columns(self)` - GŁÓWNA FUNKCJA

**Opis:** Główna logika filtrowania kolumn CSV

#### Algorytm krok po kroku:

```
1. WALIDACJA DANYCH
   ├─ Sprawdź czy wybrano plik wejściowy
   ├─ Sprawdź czy wybrano plik wyjściowy
   └─ Sprawdź czy podano fragment nazwy

2. WCZYTANIE PLIKU CSV
   ├─ Otwórz plik z encoding='utf-8'
   ├─ Użyj csv.reader z delimiter=';'
   ├─ Wczytaj wszystkie wiersze do listy
   └─ Sprawdź czy plik nie jest pusty

3. PRZETWARZANIE NAGŁÓWKÓW
   ├─ Pierwszy wiersz = nagłówki (all_columns)
   ├─ Pozostałe wiersze = dane (data_rows)
   └─ Loguj informacje o pliku

4. FILTROWANIE KOLUMN
   ├─ Inicjalizuj selected_indices = [0]  (pierwsza kolumna)
   ├─ Inicjalizuj selected_columns = [all_columns[0]]
   ├─ Dla każdej kolumny (od index 1):
   │  └─ Jeśli filter_fragment in nazwa_kolumny:
   │     ├─ Dodaj index do selected_indices
   │     └─ Dodaj nazwę do selected_columns
   └─ Sprawdź czy znaleziono jakieś kolumny

5. LOGOWANIE WYNIKÓW
   ├─ Liczba znalezionych kolumn
   ├─ Lista przykładowych kolumn (pierwsze 6)
   └─ Ostrzeżenie jeśli brak wyników

6. SPRAWDZENIE TRYBU FILTROWANIA PO GODZINIE
   ├─ Jeśli time_filter_mode == "specific_time":
   │  └─ Pobierz target_time (np. "18:00")
   └─ Loguj informację o trybie filtrowania

7. FILTROWANIE DANYCH (KOLUMNY + WIERSZE)
   ├─ Utwórz filtered_data = []
   ├─ Dodaj nagłówki wybranych kolumn
   ├─ Dla każdego wiersza danych:
   │  ├─ JEŚLI time_filter_mode == "specific_time":
   │  │  ├─ Pobierz date_str z row[0]
   │  │  ├─ Wyodrębnij część czasową (split po spacji)
   │  │  ├─ Jeśli time_part != target_time → POMIŃ wiersz
   │  │  └─ Jeśli time_part == target_time → KONTYNUUJ
   │  ├─ Ekstraktuj wartości z selected_indices
   │  └─ Dodaj do filtered_data
   └─ Sprawdź czy znaleziono jakiekolwiek wiersze

8. ZAPIS DO PLIKU
   ├─ Otwórz plik wyjściowy z encoding='utf-8'
   ├─ Użyj csv.writer z delimiter=';'
   ├─ Zapisz wszystkie wiersze (writerows)
   └─ Zamknij plik

9. POTWIERDZENIE
   ├─ Loguj sukces
   ├─ Wyświetl messagebox z potwierdzeniem
   ├─ Wyświetl statystyki (liczba wierszy przed/po filtrze, kolumn)
   └─ Jeśli time_filter_mode == "specific_time":
      └─ Dodaj informację o liczbie pominiętych wierszy

10. OBSŁUGA BŁĘDÓW
    ├─ Catch Exception
    ├─ Loguj błąd
    └─ Wyświetl messagebox z błędem
```

#### Przykład działania:

**Input:**
```
Nagłówki: ['Date UTC', 'Col1_dA', 'Col2_T', 'Col3_dA', 'Col4_X']
Fragment: '_dA'
```

**Proces:**
```
selected_indices = [0]           # Date UTC (zawsze)
selected_columns = ['Date UTC']

Iteracja 1: 'Col1_dA' contains '_dA'
  selected_indices = [0, 1]
  selected_columns = ['Date UTC', 'Col1_dA']

Iteracja 2: 'Col2_T' NOT contains '_dA'
  (pomiń)

Iteracja 3: 'Col3_dA' contains '_dA'
  selected_indices = [0, 3]
  selected_columns = ['Date UTC', 'Col1_dA', 'Col3_dA']

Iteracja 4: 'Col4_X' NOT contains '_dA'
  (pomiń)
```

**Output:**
```
Nagłówki: ['Date UTC', 'Col1_dA', 'Col3_dA']
Indeksy: [0, 1, 3]
```

#### Kod filtrowania wiersza:

```python
# Dla wiersza: ['25.09.2025', 'val1', 'val2', 'val3', 'val4']
# selected_indices = [0, 1, 3]

filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
# Wynik: ['25.09.2025', 'val1', 'val3']
```

#### Przykład z filtrowaniem po godzinie:

**Input:**
```
Nagłówki: ['Date UTC', 'Col1_dA', 'Col2_dA']
Fragment: '_dA'
Godzina: '18:00'

Data rows:
['26.09.2025 00:00', '10', '20']
['26.09.2025 12:00', '11', '21']
['26.09.2025 18:00', '12', '22']  ← PASUJE
['27.09.2025 00:00', '13', '23']
['27.09.2025 18:00', '14', '24']  ← PASUJE
```

**Proces filtrowania wierszy:**
```
Wiersz 1: '26.09.2025 00:00'
  → time_part = '00:00'
  → '00:00' != '18:00' → POMIŃ

Wiersz 2: '26.09.2025 12:00'
  → time_part = '12:00'
  → '12:00' != '18:00' → POMIŃ

Wiersz 3: '26.09.2025 18:00'
  → time_part = '18:00'
  → '18:00' == '18:00' → ZACHOWAJ

Wiersz 4: '27.09.2025 00:00'
  → time_part = '00:00'
  → '00:00' != '18:00' → POMIŃ

Wiersz 5: '27.09.2025 18:00'
  → time_part = '18:00'
  → '18:00' == '18:00' → ZACHOWAJ
```

**Output:**
```
filtered_data = [
    ['Date UTC', 'Col1_dA', 'Col2_dA'],      # Nagłówki
    ['26.09.2025 18:00', '12', '22'],        # Wiersz 3
    ['27.09.2025 18:00', '14', '24']         # Wiersz 5
]

Wierszy przed filtrowaniem: 5
Wierszy po filtrowaniu: 2
```

## Przepływ danych

```
┌─────────────────┐
│ Plik wejściowy  │
│   (CSV)         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ csv.reader()    │
│ delimiter=';'   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lista wierszy   │
│ all_rows[]      │
└────────┬────────┘
         │
         ├─────────────────┐
         ▼                 ▼
┌─────────────────┐ ┌──────────────┐
│ Nagłówki        │ │ Wiersze danych│
│ all_columns[]   │ │ data_rows[]   │
└────────┬────────┘ └──────┬───────┘
         │                 │
         │                 │
         ▼                 │
┌─────────────────┐        │
│ Filtrowanie     │        │
│ (if fragment    │        │
│  in col_name)   │        │
└────────┬────────┘        │
         │                 │
         ▼                 │
┌─────────────────┐        │
│ selected_indices│        │
│ selected_columns│        │
└────────┬────────┘        │
         │                 │
         │ ◄───────────────┘
         │
         ▼
┌─────────────────┐
│ Ekstrakcja      │
│ wartości        │
│ [row[i] for i   │
│  in indices]    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ filtered_data[] │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ csv.writer()    │
│ delimiter=';'   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Plik wyjściowy  │
│   (CSV)         │
└─────────────────┘
```

## Formaty danych

### Struktura all_rows

```python
all_rows = [
    ['Date UTC', 'Ink_[5][0]_dA', 'Ink_[5][1]_T', ...],  # Nagłówki
    ['25.09.2025 23:00', '', '', ...],                    # Wiersz 1
    ['25.09.2025 23:15', '', '', ...],                    # Wiersz 2
    ...
]
```

### Struktura selected_indices i selected_columns

```python
selected_indices = [0, 1, 3, 5, 7, ...]  # Indeksy kolumn do zachowania
selected_columns = [                     # Nazwy kolumn do zachowania
    'Date UTC',
    'Ink_[5][0]_dA',
    'Ink_[5][2]_dA',
    'Ink_[5][4]_dA',
    ...
]
```

### Struktura filtered_data

```python
filtered_data = [
    ['Date UTC', 'Ink_[5][0]_dA', 'Ink_[5][2]_dA', ...],  # Nagłówki
    ['25.09.2025 23:00', '', '', ...],                    # Wiersz 1
    ['25.09.2025 23:15', '', '', ...],                    # Wiersz 2
    ...
]
```

## Obsługa błędów

### Typy błędów i ich obsługa

1. **Brak pliku wejściowego**
   ```python
   if not self.input_file.get():
       messagebox.showerror("Błąd", "Proszę wybrać plik wejściowy!")
   ```

2. **Brak pliku wyjściowego**
   ```python
   if not self.output_file.get():
       messagebox.showerror("Błąd", "Proszę wybrać plik wyjściowy!")
   ```

3. **Brak fragmentu nazwy**
   ```python
   if not self.filter_text.get():
       messagebox.showerror("Błąd", "Proszę podać fragment nazwy kolumny!")
   ```

4. **Pusty plik CSV**
   ```python
   if not all_rows:
       messagebox.showerror("Błąd", "Plik CSV jest pusty!")
   ```

5. **Brak pasujących kolumn**
   ```python
   if len(selected_columns) == 1:
       messagebox.showwarning("Uwaga", f"Nie znaleziono...")
   ```

6. **Ogólne błędy**
   ```python
   except Exception as e:
       self.log(f"\n✗ BŁĄD: {error_msg}")
       messagebox.showerror("Błąd", error_msg)
   ```

## Optymalizacja i wydajność

### Złożoność czasowa

- **Wczytanie pliku:** O(n×m) gdzie n=liczba wierszy, m=liczba kolumn
- **Filtrowanie nagłówków:** O(m) gdzie m=liczba kolumn
- **Filtrowanie danych:** O(n×k) gdzie n=liczba wierszy, k=liczba wybranych kolumn
- **Zapis do pliku:** O(n×k)

**Całkowita złożoność:** O(n×m) + O(n×k) ≈ O(n×m)

### Zużycie pamięci

- **all_rows:** n×m wartości (cały plik w pamięci)
- **filtered_data:** n×k wartości (przefiltrowane dane)

**Całkowite zużycie:** O(n×m) + O(n×k) ≈ O(n×m)

### Możliwe optymalizacje

1. **Streaming processing:**
   ```python
   # Zamiast wczytywać cały plik:
   with open(input_file) as f_in, open(output_file, 'w') as f_out:
       reader = csv.reader(f_in, delimiter=';')
       writer = csv.writer(f_out, delimiter=';')

       headers = next(reader)
       # Filtruj nagłówki...
       writer.writerow(filtered_headers)

       for row in reader:
           filtered_row = [row[i] for i in selected_indices]
           writer.writerow(filtered_row)
   ```

   **Korzyści:** O(1) zużycie pamięci (niezależne od rozmiaru pliku)

2. **Pandas (jeśli dostępny):**
   ```python
   import pandas as pd

   df = pd.read_csv(input_file, sep=';')
   selected_cols = [col for col in df.columns if fragment in col]
   df_filtered = df[[df.columns[0]] + selected_cols]
   df_filtered.to_csv(output_file, sep=';', index=False)
   ```

   **Korzyści:** Szybsze przetwarzanie, mniej kodu

## Rozszerzenia

### 1. Obsługa wielu fragmentów

```python
# W interfejsie GUI:
tk.Label(filter_frame, text="Fragmenty (oddzielone przecinkami):").pack(...)

# W funkcji filter_columns:
fragments = [f.strip() for f in self.filter_text.get().split(',')]

for i, col in enumerate(all_columns[1:], start=1):
    if any(fragment in col for fragment in fragments):
        selected_indices.append(i)
        selected_columns.append(col)
```

### 2. Wybór separatora

```python
# W __init__:
self.separator = tk.StringVar(value=';')

# W create_widgets:
tk.Label(frame, text="Separator:").pack(side=tk.LEFT)
tk.OptionMenu(frame, self.separator, ';', ',', '\t', '|').pack(side=tk.LEFT)

# W filter_columns:
sep = self.separator.get()
reader = csv.reader(f, delimiter=sep)
writer = csv.writer(f_out, delimiter=sep)
```

### 3. Podgląd kolumn przed filtrowaniem

```python
def preview_columns(self):
    """Wyświetl listę wszystkich kolumn"""
    with open(self.input_file.get(), 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        headers = next(reader)

    preview_window = tk.Toplevel(self.root)
    preview_window.title("Podgląd kolumn")

    listbox = tk.Listbox(preview_window, width=60, height=20)
    listbox.pack(padx=10, pady=10)

    for i, col in enumerate(headers, 1):
        listbox.insert(tk.END, f"{i}. {col}")
```

### 4. Export statystyk

```python
def save_statistics(self, stats_file):
    """Zapisz statystyki do pliku"""
    stats = {
        'input_file': self.input_file.get(),
        'output_file': self.output_file.get(),
        'filter_fragment': self.filter_text.get(),
        'total_columns': len(all_columns),
        'selected_columns': len(selected_columns),
        'total_rows': len(data_rows),
        'timestamp': datetime.now().isoformat()
    }

    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
```

## Testowanie

### Unit testy

```python
import unittest

class TestCSVFilter(unittest.TestCase):
    def setUp(self):
        # Przygotuj testowe dane
        self.test_file = 'test_data.csv'
        with open(self.test_file, 'w') as f:
            f.write('Date;Col1_dA;Col2_T;Col3_dA\n')
            f.write('01.01.2025;1;2;3\n')

    def test_filter_dA_columns(self):
        # Test filtrowania kolumn _dA
        result = filter_columns(self.test_file, 'output.csv', '_dA')
        self.assertTrue(result)

        # Sprawdź wynik
        with open('output.csv') as f:
            headers = f.readline().strip().split(';')

        self.assertEqual(headers, ['Date', 'Col1_dA', 'Col3_dA'])

    def tearDown(self):
        # Usuń pliki testowe
        os.remove(self.test_file)
        os.remove('output.csv')
```

## Debugowanie

### Logi debugowania

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# W funkcji filter_columns:
logger.debug(f"Input file: {self.input_file.get()}")
logger.debug(f"Total columns: {len(all_columns)}")
logger.debug(f"Selected indices: {selected_indices}")
```

### Punkty kontrolne

```python
# Dodaj punkty kontrolne w kluczowych miejscach:
print(f"DEBUG: all_rows length = {len(all_rows)}")
print(f"DEBUG: all_columns = {all_columns[:5]}...")  # Pierwsze 5
print(f"DEBUG: selected_indices = {selected_indices}")
print(f"DEBUG: filtered_data length = {len(filtered_data)}")
```

---

**Wersja dokumentacji technicznej:** 1.0
**Data:** 2025-11-07
**Autor:** Claude & Użytkownik
