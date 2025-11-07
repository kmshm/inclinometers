#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skrypt do filtrowania kolumn w plikach CSV na podstawie fragmentu nazwy kolumny.
Zachowuje pierwszą kolumnę (daty) i wszystkie kolumny zawierające podany fragment.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import csv
import os


class CSVColumnFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtrowanie kolumn CSV")
        self.root.geometry("700x700")

        # Zmienne
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.filter_text = tk.StringVar(value="_dA")

        # Zmienne dla filtrowania po godzinie
        self.time_filter_mode = tk.StringVar(value="all")  # "all" lub "specific_time"
        self.specific_time = tk.StringVar(value="18:00")

        # Zmienne dla filtrowania po inklinometrze
        self.inclinometer_filter_enabled = tk.BooleanVar(value=False)
        self.inclinometer_name = tk.StringVar(value="Inkl_[1]")

        # Zmienne dla generowania osobnych plików
        self.split_by_inclinometer = tk.BooleanVar(value=False)
        self.base_filename = tk.StringVar(value="")

        # Tworzenie interfejsu
        self.create_widgets()

    def create_widgets(self):
        # Ramka dla pliku wejściowego
        input_frame = tk.Frame(self.root, padx=10, pady=5)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Plik wejściowy:").pack(side=tk.LEFT)
        tk.Entry(input_frame, textvariable=self.input_file, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(input_frame, text="Wybierz...", command=self.select_input_file).pack(side=tk.LEFT)

        # Ramka dla fragmentu nazwy kolumny
        filter_frame = tk.Frame(self.root, padx=10, pady=5)
        filter_frame.pack(fill=tk.X)

        tk.Label(filter_frame, text="Fragment nazwy kolumny:").pack(side=tk.LEFT)
        tk.Entry(filter_frame, textvariable=self.filter_text, width=20).pack(side=tk.LEFT, padx=5)
        tk.Label(filter_frame, text="(np. _dA, _T, _dB)").pack(side=tk.LEFT)

        # Ramka dla filtrowania po inklinometrze
        inclinometer_frame = tk.Frame(self.root, padx=10, pady=5)
        inclinometer_frame.pack(fill=tk.X)

        self.inclinometer_checkbox = tk.Checkbutton(
            inclinometer_frame,
            text="Tylko z konkretnego inklinometru:",
            variable=self.inclinometer_filter_enabled,
            command=self.toggle_inclinometer_input
        )
        self.inclinometer_checkbox.pack(side=tk.LEFT)

        self.inclinometer_entry = tk.Entry(
            inclinometer_frame,
            textvariable=self.inclinometer_name,
            width=15
        )
        self.inclinometer_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(inclinometer_frame, text="(np. Inkl_[1], Ink_[5])").pack(side=tk.LEFT)

        # Początkowy stan - wyłącz pole inklinometru
        self.inclinometer_entry.config(state='disabled')

        # Ramka dla filtrowania po godzinie
        time_filter_frame = tk.Frame(self.root, padx=10, pady=5)
        time_filter_frame.pack(fill=tk.X)

        tk.Label(time_filter_frame, text="Filtrowanie wierszy:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

        # Radio buttons dla opcji
        radio_frame = tk.Frame(time_filter_frame, padx=20, pady=5)
        radio_frame.pack(fill=tk.X)

        tk.Radiobutton(radio_frame, text="Wszystkie dane (pełne wiersze)",
                      variable=self.time_filter_mode, value="all",
                      command=self.toggle_time_input).pack(anchor=tk.W)

        time_specific_frame = tk.Frame(radio_frame)
        time_specific_frame.pack(anchor=tk.W, pady=2)

        tk.Radiobutton(time_specific_frame, text="Tylko wiersze z konkretną godziną:",
                      variable=self.time_filter_mode, value="specific_time",
                      command=self.toggle_time_input).pack(side=tk.LEFT)

        self.time_entry = tk.Entry(time_specific_frame, textvariable=self.specific_time, width=10)
        self.time_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(time_specific_frame, text="(format HH:MM, np. 18:00)").pack(side=tk.LEFT)

        # Początkowy stan - wyłącz pole czasu
        self.time_entry.config(state='disabled')

        # Ramka dla opcji generowania osobnych plików
        split_frame = tk.Frame(self.root, padx=10, pady=5)
        split_frame.pack(fill=tk.X)

        split_label_frame = tk.Frame(split_frame)
        split_label_frame.pack(anchor=tk.W, pady=2)

        self.split_checkbox = tk.Checkbutton(
            split_label_frame,
            text="Generuj osobne pliki dla każdego inklinometru",
            variable=self.split_by_inclinometer,
            command=self.toggle_split_mode
        )
        self.split_checkbox.pack(side=tk.LEFT)

        split_input_frame = tk.Frame(split_frame, padx=20)
        split_input_frame.pack(anchor=tk.W, pady=2)

        tk.Label(split_input_frame, text="Nazwa bazowa:").pack(side=tk.LEFT)
        self.base_filename_entry = tk.Entry(split_input_frame, textvariable=self.base_filename, width=30)
        self.base_filename_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(split_input_frame, text="(np. 'dane_12_00')").pack(side=tk.LEFT)

        # Początkowy stan - wyłącz pole nazwy bazowej
        self.base_filename_entry.config(state='disabled')

        # Ramka dla pliku wyjściowego
        output_frame = tk.Frame(self.root, padx=10, pady=5)
        output_frame.pack(fill=tk.X)

        self.output_label = tk.Label(output_frame, text="Plik wyjściowy:")
        self.output_label.pack(side=tk.LEFT)
        self.output_entry = tk.Entry(output_frame, textvariable=self.output_file, width=50)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        self.output_button = tk.Button(output_frame, text="Wybierz...", command=self.select_output_file)
        self.output_button.pack(side=tk.LEFT)

        # Przycisk filtrowania
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Filtruj kolumny", command=self.filter_columns,
                 bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                 height=2).pack(expand=True)

        # Pole tekstowe dla logów
        log_frame = tk.Frame(self.root, padx=10, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="Logi:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """Dodaje wiadomość do okna logów"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def select_input_file(self):
        """Wybór pliku wejściowego"""
        filename = filedialog.askopenfilename(
            title="Wybierz plik CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Automatyczne ustawienie nazwy pliku wyjściowego
            if not self.output_file.get():
                base, ext = os.path.splitext(filename)
                self.output_file.set(f"{base}_filtered{ext}")

    def select_output_file(self):
        """Wybór pliku wyjściowego"""
        filename = filedialog.asksaveasfilename(
            title="Zapisz jako",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)

    def toggle_time_input(self):
        """Włącz/wyłącz pole wprowadzania godziny"""
        if self.time_filter_mode.get() == "specific_time":
            self.time_entry.config(state='normal')
        else:
            self.time_entry.config(state='disabled')

    def toggle_inclinometer_input(self):
        """Włącz/wyłącz pole wprowadzania inklinometru"""
        if self.inclinometer_filter_enabled.get():
            self.inclinometer_entry.config(state='normal')
        else:
            self.inclinometer_entry.config(state='disabled')

    def toggle_split_mode(self):
        """Włącz/wyłącz tryb generowania osobnych plików"""
        if self.split_by_inclinometer.get():
            # Włącz pole nazwy bazowej
            self.base_filename_entry.config(state='normal')
            # Wyłącz pojedynczy inklinometr
            self.inclinometer_filter_enabled.set(False)
            self.inclinometer_checkbox.config(state='disabled')
            self.inclinometer_entry.config(state='disabled')
            # Wyłącz wybór pojedynczego pliku wyjściowego
            self.output_label.config(text="Folder wyjściowy:")
            self.output_entry.config(state='disabled')
            self.output_button.config(state='disabled')
        else:
            # Wyłącz pole nazwy bazowej
            self.base_filename_entry.config(state='disabled')
            # Włącz pojedynczy inklinometr
            self.inclinometer_checkbox.config(state='normal')
            # Włącz wybór pojedynczego pliku wyjściowego
            self.output_label.config(text="Plik wyjściowy:")
            self.output_entry.config(state='normal')
            self.output_button.config(state='normal')

    def detect_inclinometers(self, columns):
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

    def calculate_max_value(self, row, column_names):
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

    def filter_columns(self):
        """Główna funkcja filtrująca kolumny"""
        # Walidacja
        if not self.input_file.get():
            messagebox.showerror("Błąd", "Proszę wybrać plik wejściowy!")
            return

        # Sprawdź czy tryb split jest włączony
        split_mode = self.split_by_inclinometer.get()

        if split_mode:
            if not self.base_filename.get():
                messagebox.showerror("Błąd", "Proszę podać nazwę bazową pliku!")
                return
        else:
            if not self.output_file.get():
                messagebox.showerror("Błąd", "Proszę wybrać plik wyjściowy!")
                return

        if not self.filter_text.get():
            messagebox.showerror("Błąd", "Proszę podać fragment nazwy kolumny!")
            return

        try:
            self.log_text.delete(1.0, tk.END)  # Czyszczenie logów
            self.log("=" * 60)
            self.log("Rozpoczynam filtrowanie...")
            self.log(f"Plik wejściowy: {self.input_file.get()}")
            self.log(f"Fragment nazwy: '{self.filter_text.get()}'")

            # Wczytanie pliku CSV
            self.log("\nWczytywanie pliku CSV...")
            with open(self.input_file.get(), 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                all_rows = list(reader)

            if not all_rows:
                messagebox.showerror("Błąd", "Plik CSV jest pusty!")
                return

            # Pobierz nagłówki (pierwszy wiersz)
            all_columns = all_rows[0]
            data_rows = all_rows[1:]

            self.log(f"Wczytano {len(data_rows)} wierszy i {len(all_columns)} kolumn")
            self.log(f"\nPierwsza kolumna (daty): {all_columns[0]}")

            # Filtrowanie kolumn - pierwsza kolumna + kolumny zawierające fragment
            filter_fragment = self.filter_text.get()

            # TRYB SPLIT: Generuj osobne pliki dla każdego inklinometru
            if split_mode:
                self.log("\n*** TRYB: Generowanie osobnych plików dla każdego inklinometru ***")

                # Wykryj wszystkie inklinometry
                inclinometers = self.detect_inclinometers(all_columns)
                self.log(f"\nZnaleziono {len(inclinometers)} inklinometrów: {', '.join(inclinometers)}")

                if not inclinometers:
                    messagebox.showerror("Błąd", "Nie znaleziono żadnych inklinometrów w pliku!")
                    self.log("\n⚠ BŁĄD: Brak inklinometrów w nagłówkach")
                    return

                # Pobierz folder i nazwę bazową
                input_dir = os.path.dirname(self.input_file.get()) or '.'
                base_name = self.base_filename.get().strip()

                files_created = []

                # Przetwórz każdy inklinometr
                for inclinometer in inclinometers:
                    self.log(f"\n--- Przetwarzanie: {inclinometer} ---")

                    # Filtruj kolumny dla tego inklinometru
                    selected_indices = [0]
                    selected_columns = [all_columns[0]]

                    for i, col in enumerate(all_columns[1:], start=1):
                        if filter_fragment in col and col.startswith(inclinometer):
                            selected_indices.append(i)
                            selected_columns.append(col)

                    if len(selected_columns) == 1:
                        self.log(f"  ⚠ Brak kolumn zawierających '{filter_fragment}' dla {inclinometer}, pomijam")
                        continue

                    self.log(f"  Znaleziono {len(selected_columns) - 1} kolumn")

                    # Filtrowanie po godzinie (jeśli wybrano)
                    time_mode = self.time_filter_mode.get()
                    if time_mode == "specific_time":
                        target_time = self.specific_time.get().strip()
                        self.log(f"  Filtrowanie po godzinie: {target_time}")

                        filtered_rows = []
                        for row in data_rows:
                            if len(row) > 0:
                                date_str = row[0].strip()
                                if ' ' in date_str:
                                    time_part = date_str.split(' ')[-1]
                                    if time_part == target_time:
                                        filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                                        filtered_rows.append(filtered_row)
                    else:
                        filtered_rows = []
                        for row in data_rows:
                            filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                            filtered_rows.append(filtered_row)

                    self.log(f"  Wierszy: {len(filtered_rows)}")

                    # Dodaj kolumny MAX i MAX_COLUMN
                    extended_columns = selected_columns + ['MAX', 'MAX_COLUMN']

                    # Oblicz MAX i MAX_COLUMN dla każdego wiersza
                    extended_rows = []
                    for filtered_row in filtered_rows:
                        max_val, max_col = self.calculate_max_value(filtered_row, selected_columns)

                        # Dodaj wartości MAX i MAX_COLUMN na końcu wiersza
                        extended_row = filtered_row + [
                            str(max_val) if max_val is not None else '',
                            max_col if max_col is not None else ''
                        ]
                        extended_rows.append(extended_row)

                    # Utwórz nazwę pliku
                    # Zamień [ i ] na _ dla bezpiecznej nazwy pliku
                    safe_incl_name = inclinometer.replace('[', '_').replace(']', '_').replace('__', '_').rstrip('_')
                    output_filename = f"{base_name}_{safe_incl_name}.csv"
                    output_path = os.path.join(input_dir, output_filename)

                    # Zapisz plik
                    with open(output_path, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f, delimiter=';')
                        writer.writerow(extended_columns)
                        writer.writerows(extended_rows)

                    files_created.append(output_filename)
                    self.log(f"  ✓ Zapisano: {output_filename}")

                self.log("\n" + "=" * 60)
                self.log(f"✓ SUKCES! Utworzono {len(files_created)} plików:")
                for fname in files_created:
                    self.log(f"  - {fname}")
                self.log("=" * 60)

                messagebox.showinfo("Sukces",
                    f"Utworzono {len(files_created)} plików!\n\n" +
                    "\n".join([f"- {f}" for f in files_created[:5]]) +
                    (f"\n... i {len(files_created) - 5} więcej" if len(files_created) > 5 else ""))
                return

            # TRYB NORMALNY: Pojedynczy plik
            # Sprawdź czy filtrujemy po inklinometrze
            inclinometer_filter = self.inclinometer_filter_enabled.get()
            if inclinometer_filter:
                inclinometer = self.inclinometer_name.get().strip()
                self.log(f"Filtrowanie po inklinometrze: {inclinometer}")

            # Znajdź indeksy kolumn do zachowania
            selected_indices = [0]  # Pierwsza kolumna (daty)
            selected_columns = [all_columns[0]]

            # Dodaj kolumny zawierające fragment, zachowując kolejność
            for i, col in enumerate(all_columns[1:], start=1):
                # Sprawdź fragment nazwy
                if filter_fragment in col:
                    # Jeśli filtrujemy po inklinometrze, sprawdź czy kolumna należy do tego inklinometru
                    if inclinometer_filter:
                        if col.startswith(inclinometer):
                            selected_indices.append(i)
                            selected_columns.append(col)
                    else:
                        selected_indices.append(i)
                        selected_columns.append(col)

            self.log(f"\nZnaleziono {len(selected_columns) - 1} kolumn zawierających '{filter_fragment}'")
            if inclinometer_filter:
                self.log(f"  (tylko z inklinometru {inclinometer})")
            self.log(f"Łącznie kolumn w nowym pliku: {len(selected_columns)} (włącznie z kolumną dat)")

            if len(selected_columns) == 1:
                messagebox.showwarning("Uwaga",
                    f"Nie znaleziono żadnych kolumn zawierających '{filter_fragment}'!")
                self.log("\n⚠ UWAGA: Nie znaleziono żadnych pasujących kolumn!")
                return

            # Przykładowe kolumny (pierwsze 5)
            self.log("\nPrzykładowe wybrane kolumny:")
            for i, col in enumerate(selected_columns[:6], 1):
                self.log(f"  {i}. {col}")
            if len(selected_columns) > 6:
                self.log(f"  ... i {len(selected_columns) - 6} więcej")

            # Filtrowanie danych
            self.log("\nTworzenie przefiltrowanego pliku...")

            # Sprawdź tryb filtrowania po godzinie
            time_mode = self.time_filter_mode.get()
            if time_mode == "specific_time":
                target_time = self.specific_time.get().strip()
                self.log(f"Filtrowanie wierszy - tylko godzina: {target_time}")
            else:
                self.log("Filtrowanie wierszy - wszystkie dane")

            filtered_data = []
            filtered_data.append(selected_columns)  # Nagłówki

            rows_before_time_filter = len(data_rows)
            rows_after_time_filter = 0

            for row in data_rows:
                # Filtrowanie po godzinie (jeśli wybrano)
                if time_mode == "specific_time":
                    # Sprawdź czy pierwsza kolumna (data) zawiera podaną godzinę
                    if len(row) > 0:
                        date_str = row[0].strip()
                        # Format: "DD.MM.YYYY HH:MM"
                        # Pobierz część czasu (po spacji)
                        if ' ' in date_str:
                            time_part = date_str.split(' ')[-1]  # Ostatnia część po spacji
                            if time_part != target_time:
                                continue  # Pomiń ten wiersz
                        else:
                            continue  # Brak czasu w formacie, pomiń
                    else:
                        continue  # Pusty wiersz, pomiń

                # Wybierz tylko kolumny według selected_indices
                filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                filtered_data.append(filtered_row)
                rows_after_time_filter += 1

            # Informacje o filtrowaniu po godzinie
            if time_mode == "specific_time":
                self.log(f"\nWierszy przed filtrowaniem po godzinie: {rows_before_time_filter}")
                self.log(f"Wierszy po filtrowaniu (tylko {target_time}): {rows_after_time_filter}")
                if rows_after_time_filter == 0:
                    messagebox.showwarning("Uwaga",
                        f"Nie znaleziono żadnych wierszy z godziną {target_time}!\n"
                        f"Sprawdź czy godzina jest w formacie HH:MM (np. 18:00)")
                    self.log("\n⚠ UWAGA: Nie znaleziono żadnych wierszy z podaną godziną!")
                    return

            # Zapisanie do pliku
            self.log(f"\nZapisywanie do: {self.output_file.get()}")
            with open(self.output_file.get(), 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(filtered_data)

            self.log("\n✓ Sukces! Plik został zapisany.")
            if time_mode == "specific_time":
                self.log(f"✓ Zapisano {rows_after_time_filter} wierszy (z {rows_before_time_filter}) i {len(selected_columns)} kolumn")
            else:
                self.log(f"✓ Zapisano {rows_after_time_filter} wierszy i {len(selected_columns)} kolumn")
            self.log("=" * 60)

            # Komunikat sukcesu
            success_msg = f"Plik został pomyślnie przefiltrowany!\n\n"
            if time_mode == "specific_time":
                success_msg += f"Wierszy (tylko godzina {target_time}): {rows_after_time_filter}\n"
                success_msg += f"Wierszy pominięto: {rows_before_time_filter - rows_after_time_filter}\n"
            else:
                success_msg += f"Wierszy: {rows_after_time_filter}\n"
            success_msg += f"Kolumny: {len(selected_columns)}\n"
            success_msg += f"Zapisano jako: {os.path.basename(self.output_file.get())}"

            messagebox.showinfo("Sukces", success_msg)

        except Exception as e:
            error_msg = f"Wystąpił błąd: {str(e)}"
            self.log(f"\n✗ BŁĄD: {error_msg}")
            messagebox.showerror("Błąd", error_msg)


def main():
    root = tk.Tk()
    app = CSVColumnFilterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
