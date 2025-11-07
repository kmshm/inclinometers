#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prosty test funkcjonalności filtrowania kolumn CSV
"""

import csv

def test_filter_columns(input_file, output_file, filter_fragment):
    """Test funkcji filtrowania kolumn"""

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
    print(f"Łącznie kolumn: {len(selected_columns)}")

    if len(selected_columns) == 1:
        print("UWAGA: Nie znaleziono żadnych pasujących kolumn!")
        return False

    # Przykładowe kolumny
    print("\nPrzykładowe wybrane kolumny:")
    for i, col in enumerate(selected_columns[:10], 1):
        print(f"  {i}. {col}")
    if len(selected_columns) > 10:
        print(f"  ... i {len(selected_columns) - 10} więcej")

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
    # Test z plikiem testowe.csv
    print("=" * 60)
    print("TEST: Filtrowanie kolumn zawierających '_dA'")
    print("=" * 60)

    test_filter_columns(
        "testowe.csv",
        "testowe_filtered_dA.csv",
        "_dA"
    )

    print("\n" + "=" * 60)
    print("TEST: Filtrowanie kolumn zawierających '_T'")
    print("=" * 60)

    test_filter_columns(
        "testowe.csv",
        "testowe_filtered_T.csv",
        "_T"
    )
