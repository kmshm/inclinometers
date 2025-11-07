#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test funkcji filtrowania po inklinometrze
"""

import csv
import os

def test_inclinometer_filter(input_file, output_file, filter_fragment, inclinometer=None, target_time=None):
    """
    Test funkcji filtrowania kolumn z opcjonalnym filtrowaniem po inklinometrze i godzinie

    Args:
        input_file: ścieżka do pliku wejściowego
        output_file: ścieżka do pliku wyjściowego
        filter_fragment: fragment nazwy kolumny (np. "_dA")
        inclinometer: nazwa inklinometru (np. "Inkl_[1]") lub None
        target_time: godzina do filtrowania (np. "18:00") lub None
    """

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
        # Sprawdź fragment nazwy
        if filter_fragment in col:
            # Jeśli filtrujemy po inklinometrze, sprawdź czy kolumna należy do tego inklinometru
            if inclinometer:
                if col.startswith(inclinometer):
                    selected_indices.append(i)
                    selected_columns.append(col)
            else:
                selected_indices.append(i)
                selected_columns.append(col)

    print(f"\nZnaleziono {len(selected_columns) - 1} kolumn zawierających '{filter_fragment}'")
    if inclinometer:
        print(f"  (tylko z inklinometru {inclinometer})")

    if len(selected_columns) == 1:
        print(f"\n⚠ UWAGA: Nie znaleziono żadnych pasujących kolumn!")
        return False

    # Przykładowe kolumny
    print("\nPrzykładowe wybrane kolumny:")
    for i, col in enumerate(selected_columns[:10], 1):
        print(f"  {i}. {col}")
    if len(selected_columns) > 10:
        print(f"  ... i {len(selected_columns) - 10} więcej")

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
    # Utwórz folder test_outputs jeśli nie istnieje
    os.makedirs("test_outputs", exist_ok=True)

    print("=" * 60)
    print("TEST 1: Wszystkie inklinometry, kolumny _dA")
    print("=" * 60)
    test_inclinometer_filter(
        "testowe.csv",
        "test_outputs/test_all_inclinometers_dA.csv",
        "_dA",
        inclinometer=None
    )

    print("\n" + "=" * 60)
    print("TEST 2: Tylko Inkl_[1], kolumny _dA")
    print("=" * 60)
    test_inclinometer_filter(
        "testowe.csv",
        "test_outputs/test_Inkl1_dA.csv",
        "_dA",
        inclinometer="Inkl_[1]"
    )

    print("\n" + "=" * 60)
    print("TEST 3: Tylko Inkl_[2], kolumny _T")
    print("=" * 60)
    test_inclinometer_filter(
        "testowe.csv",
        "test_outputs/test_Inkl2_T.csv",
        "_T",
        inclinometer="Inkl_[2]"
    )

    print("\n" + "=" * 60)
    print("TEST 4: Tylko Ink_[6], kolumny _dB")
    print("=" * 60)
    test_inclinometer_filter(
        "testowe.csv",
        "test_outputs/test_Ink6_dB.csv",
        "_dB",
        inclinometer="Ink_[6]"
    )

    print("\n" + "=" * 60)
    print("TEST 5: Tylko Inkl_[1], kolumny _dA, godzina 00:00")
    print("=" * 60)
    test_inclinometer_filter(
        "testowe.csv",
        "test_outputs/test_Inkl1_dA_00_00.csv",
        "_dA",
        inclinometer="Inkl_[1]",
        target_time="00:00"
    )

    print("\n" + "=" * 60)
    print("TEST 6: Tylko Inkl_[3], kolumny _X, godzina 12:00")
    print("=" * 60)
    test_inclinometer_filter(
        "testowe.csv",
        "test_outputs/test_Inkl3_X_12_00.csv",
        "_X",
        inclinometer="Inkl_[3]",
        target_time="12:00"
    )
