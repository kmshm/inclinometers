#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test funkcji filtrowania po godzinie
"""

import csv

def test_time_filter(input_file, output_file, filter_fragment, target_time=None):
    """Test funkcji filtrowania kolumn z opcjonalnym filtrowaniem po godzinie"""

    # Wczytanie pliku CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        all_rows = list(reader)

    if not all_rows:
        print("Błąd: Plik CSV jest pusty!")
        return False

    # Pobierz nagłówki
    all_columns = all_rows[0]
    data_rows = all_rows[1:]

    print(f"Wczytano {len(data_rows)} wierszy i {len(all_columns)} kolumn")
    print(f"Pierwsza kolumna (daty): {all_columns[0]}")

    # Filtrowanie kolumn
    selected_indices = [0]  # Pierwsza kolumna
    selected_columns = [all_columns[0]]

    for i, col in enumerate(all_columns[1:], start=1):
        if filter_fragment in col:
            selected_indices.append(i)
            selected_columns.append(col)

    print(f"\nZnaleziono {len(selected_columns) - 1} kolumn zawierających '{filter_fragment}'")

    # Filtrowanie po godzinie (jeśli podano)
    if target_time:
        print(f"\nFiltrowanie wierszy - tylko godzina: {target_time}")
        rows_before = len(data_rows)
        filtered_rows = []

        for row in data_rows:
            if len(row) > 0:
                date_str = row[0].strip()
                if ' ' in date_str:
                    time_part = date_str.split(' ')[-1]
                    if time_part == target_time:
                        filtered_rows.append(row)

        data_rows = filtered_rows
        print(f"Wierszy przed filtrowaniem: {rows_before}")
        print(f"Wierszy po filtrowaniu: {len(data_rows)}")

        if len(data_rows) == 0:
            print(f"\n⚠ UWAGA: Nie znaleziono żadnych wierszy z godziną {target_time}!")
            return False
    else:
        print("\nFiltrowanie wierszy - wszystkie dane")

    # Filtrowanie danych
    filtered_data = [selected_columns]
    for row in data_rows:
        filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
        filtered_data.append(filtered_row)

    # Zapisanie do pliku
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(filtered_data)

    print(f"\n✓ Sukces! Zapisano {len(data_rows)} wierszy i {len(selected_columns)} kolumn")
    print(f"✓ Plik wyjściowy: {output_file}")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("TEST 1: Wszystkie dane (kolumny _dA)")
    print("=" * 60)
    test_time_filter(
        "testowe.csv",
        "test_all_data.csv",
        "_dA",
        target_time=None
    )

    print("\n" + "=" * 60)
    print("TEST 2: Tylko godzina 00:00 (kolumny _dA)")
    print("=" * 60)
    test_time_filter(
        "testowe.csv",
        "test_00_00.csv",
        "_dA",
        target_time="00:00"
    )

    print("\n" + "=" * 60)
    print("TEST 3: Tylko godzina 12:00 (kolumny _T)")
    print("=" * 60)
    test_time_filter(
        "testowe.csv",
        "test_12_00_T.csv",
        "_T",
        target_time="12:00"
    )

    print("\n" + "=" * 60)
    print("TEST 4: Tylko godzina 23:00 (kolumny _dB)")
    print("=" * 60)
    test_time_filter(
        "testowe.csv",
        "test_23_00_dB.csv",
        "_dB",
        target_time="23:00"
    )
