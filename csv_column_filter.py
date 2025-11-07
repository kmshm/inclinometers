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
        self.root.geometry("700x500")

        # Zmienne
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.filter_text = tk.StringVar(value="_dA")

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

        # Ramka dla pliku wyjściowego
        output_frame = tk.Frame(self.root, padx=10, pady=5)
        output_frame.pack(fill=tk.X)

        tk.Label(output_frame, text="Plik wyjściowy:").pack(side=tk.LEFT)
        tk.Entry(output_frame, textvariable=self.output_file, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Wybierz...", command=self.select_output_file).pack(side=tk.LEFT)

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

    def filter_columns(self):
        """Główna funkcja filtrująca kolumny"""
        # Walidacja
        if not self.input_file.get():
            messagebox.showerror("Błąd", "Proszę wybrać plik wejściowy!")
            return

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

            # Znajdź indeksy kolumn do zachowania
            selected_indices = [0]  # Pierwsza kolumna (daty)
            selected_columns = [all_columns[0]]

            # Dodaj kolumny zawierające fragment, zachowując kolejność
            for i, col in enumerate(all_columns[1:], start=1):
                if filter_fragment in col:
                    selected_indices.append(i)
                    selected_columns.append(col)

            self.log(f"\nZnaleziono {len(selected_columns) - 1} kolumn zawierających '{filter_fragment}'")
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
            filtered_data = []
            filtered_data.append(selected_columns)  # Nagłówki

            for row in data_rows:
                filtered_row = [row[i] if i < len(row) else '' for i in selected_indices]
                filtered_data.append(filtered_row)

            # Zapisanie do pliku
            self.log(f"Zapisywanie do: {self.output_file.get()}")
            with open(self.output_file.get(), 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerows(filtered_data)

            self.log("\n✓ Sukces! Plik został zapisany.")
            self.log(f"✓ Zapisano {len(data_rows)} wierszy i {len(selected_columns)} kolumn")
            self.log("=" * 60)

            messagebox.showinfo("Sukces",
                f"Plik został pomyślnie przefiltrowany!\n\n"
                f"Wiersze: {len(data_rows)}\n"
                f"Kolumny: {len(selected_columns)}\n"
                f"Zapisano jako: {os.path.basename(self.output_file.get())}")

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
