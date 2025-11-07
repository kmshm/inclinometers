#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test funkcji generowania osobnych plików dla każdego inklinometru
"""

import csv
import os
import glob

def detect_inclinometers(columns):
    """Wykryj wszystkie unikalne inklinometry w nagłówkach kolumn"""
    inclinometers = set()
    for col in columns[1:]:  # Pomiń pierwszą kolumnę (daty)
        # Szukaj wzorców: Inkl_[x] lub Ink_[x]
        if col.startswith('Inkl_[') or col.startswith('Ink_['):
            # Pobierz część do drugiego nawiasu ']'
            parts = col.split(']')
            if len(parts) >= 2:
                inclinometer = parts[0] + ']'  # np. "Inkl_[1]" lub "Ink_[6]"
                inclinometers.add(inclinometer)
    return sorted(list(inclinometers))


def calculate_max_value(row, column_names):
    """
    Oblicz maksymalną wartość z wiersza i znajdź jej źródło

    Args:
        row: wiersz danych (lista wartości, pierwsza to data)
        column_names: nazwy kolumn (lista, pierwsza to Date UTC)

    Returns:
        (max_value, max_column_name) lub (None, None) jeśli brak wartości numerycznych
    """
    max_val = None
    max_col = None

    # Pomiń pierwszą kolumnę (daty) - start od indeksu 1
    for i in range(1, len(row)):
        value_str = row[i].strip() if i < len(row) else ''

        if value_str and value_str != '':
            try:
                value = float(value_str)
                if max_val is None or value > max_val:
                    max_val = value
                    max_col = column_names[i] if i < len(column_names) else f"Column_{i}"
            except ValueError:
                # Wartość nie jest liczbą, pomiń
                continue

    return (max_val, max_col)


def split_by_inclinometer(input_file, base_filename, filter_fragment, target_time=None):
    """
    Generuj osobne pliki dla każdego inklinometru

    Args:
        input_file: ścieżka do pliku wejściowego
        base_filename: bazowa nazwa pliku (bez rozszerzenia)
        filter_fragment: fragment nazwy kolumny (np. "_dA")
        target_time: godzina do filtrowania (np. "18:00") lub None
    """

    print(f"Plik wejściowy: {input_file}")
    print(f"Nazwa bazowa: {base_filename}")
    print(f"Fragment: {filter_fragment}")
    if target_time:
        print(f"Godzina: {target_time}")

    # Wczytanie pliku CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        all_rows = list(reader)

    if not all_rows:
        print("Błąd: Plik CSV jest pusty!")
        return []

    # Pobierz nagłówki
    all_columns = all_rows[0]
    data_rows = all_rows[1:]

    print(f"\nWczytano {len(data_rows)} wierszy i {len(all_columns)} kolumn")

    # Wykryj inklinometry
    inclinometers = detect_inclinometers(all_columns)
    print(f"Znaleziono {len(inclinometers)} inklinometrów: {', '.join(inclinometers)}")

    if not inclinometers:
        print("⚠ Brak inklinometrów w nagłówkach")
        return []

    # Pobierz folder wyjściowy
    input_dir = os.path.dirname(input_file) or '.'
    output_dir = os.path.join(input_dir, "test_outputs")
    os.makedirs(output_dir, exist_ok=True)

    files_created = []

    # Przetwórz każdy inklinometr
    for inclinometer in inclinometers:
        print(f"\n--- Przetwarzanie: {inclinometer} ---")

        # Filtruj kolumny dla tego inklinometru
        selected_indices = [0]
        selected_columns = [all_columns[0]]

        for i, col in enumerate(all_columns[1:], start=1):
            if filter_fragment in col and col.startswith(inclinometer):
                selected_indices.append(i)
                selected_columns.append(col)

        if len(selected_columns) == 1:
            print(f"  ⚠ Brak kolumn zawierających '{filter_fragment}', pomijam")
            continue

        print(f"  Znaleziono {len(selected_columns) - 1} kolumn")

        # Filtrowanie po godzinie (jeśli podano)
        if target_time:
            filtered_rows = []
            for row in data_rows:
                if len(row) > 0:
                    date_str = row[0].strip()
                    if ' ' in date_str:
                        time_part = date_str.split(' ')[-1]
                        if time_part == target_time:
                            filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                            filtered_rows.append(filtered_row)
            print(f"  Wierszy po filtrowaniu czasu: {len(filtered_rows)}")
        else:
            filtered_rows = []
            for row in data_rows:
                filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                filtered_rows.append(filtered_row)
            print(f"  Wierszy: {len(filtered_rows)}")

        # Dodaj kolumny MAX i MAX_COLUMN
        extended_columns = selected_columns + ['MAX', 'MAX_COLUMN']

        # Oblicz MAX i MAX_COLUMN dla każdego wiersza
        extended_rows = []
        for filtered_row in filtered_rows:
            max_val, max_col = calculate_max_value(filtered_row, selected_columns)

            # Dodaj wartości MAX i MAX_COLUMN na końcu wiersza
            extended_row = filtered_row + [
                str(max_val) if max_val is not None else '',
                max_col if max_col is not None else ''
            ]
            extended_rows.append(extended_row)

        print(f"  Dodano kolumny MAX i MAX_COLUMN")

        # Utwórz nazwę pliku
        safe_incl_name = inclinometer.replace('[', '_').replace(']', '_').replace('__', '_').rstrip('_')
        output_filename = f"{base_filename}_{safe_incl_name}.csv"
        output_path = os.path.join(output_dir, output_filename)

        # Zapisz plik
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(extended_columns)
            writer.writerows(extended_rows)

        files_created.append(output_filename)
        print(f"  ✓ Zapisano: {output_filename}")

    return files_created


if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: Split po inklinometrach, wszystkie wiersze, kolumny _dA")
    print("=" * 60)
    files = split_by_inclinometer(
        "testowe.csv",
        "test_split_all_dA",
        "_dA",
        target_time=None
    )
    print(f"\n✓ Utworzono {len(files)} plików")

    print("\n" + "=" * 60)
    print("TEST 2: Split po inklinometrach, godzina 12:00, kolumny _T")
    print("=" * 60)
    files = split_by_inclinometer(
        "testowe.csv",
        "test_split_12_00_T",
        "_T",
        target_time="12:00"
    )
    print(f"\n✓ Utworzono {len(files)} plików")

    print("\n" + "=" * 60)
    print("TEST 3: Split po inklinometrach, godzina 00:00, kolumny _dB")
    print("=" * 60)
    files = split_by_inclinometer(
        "testowe.csv",
        "test_split_00_00_dB",
        "_dB",
        target_time="00:00"
    )
    print(f"\n✓ Utworzono {len(files)} plików")

    # Pokaż przykładowy plik
    print("\n" + "=" * 60)
    print("Przykład zawartości pliku (test_split_12_00_T_Inkl_1.csv):")
    print("=" * 60)
    example_file = "test_outputs/test_split_12_00_T_Inkl_1.csv"
    if os.path.exists(example_file):
        with open(example_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 5:  # Pierwsze 5 linii
                    cols = line.strip().split(';')
                    print(f"  {';'.join(cols[:5])}..." if len(cols) > 5 else f"  {line.strip()}")

    # Pokaż wszystkie utworzone pliki
    print("\n" + "=" * 60)
    print("Wszystkie utworzone pliki split:")
    print("=" * 60)
    split_files = glob.glob("test_outputs/test_split_*.csv")
    for f in sorted(split_files):
        size = os.path.getsize(f)
        print(f"  {os.path.basename(f)} ({size} bytes)")
