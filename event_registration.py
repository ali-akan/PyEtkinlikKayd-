import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

CSV_FILE = 'katilimcilar.csv'

def create_csv_file():
    """Create the CSV file if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["İsim", "Soyisim", "Doğum Tarihi"])

def is_valid_date(date_text):
    """Check if the date string is a valid date."""
    try:
        datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def is_valid_input(name, surname, dob):
    """Check if the input fields are valid."""
    if not name or not surname or not dob:
        raise ValueError("Tüm alanları doldurun!")
    if not is_valid_date(dob):
        raise ValueError("Doğru tarih formatını kullanın (Gün/Ay/Yıl)")

def check_existing_record(name, surname, dob):
    """Check if a record already exists in the CSV file."""
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower() == name.lower() and row[1].lower() == surname.lower() and row[2] == dob:
                return True
    return False

def save_entry(name, surname, dob, combo_records):
    """Save entry to the CSV file."""
    try:
        is_valid_input(name, surname, dob)
        
        if check_existing_record(name, surname, dob):
            messagebox.showinfo("Bilgi", "Bu kayıt zaten mevcut.")
            return

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, surname, dob])

        messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi!")
        combo_records['values'] = load_records()
    except ValueError as e:
        messagebox.showerror("Hata", str(e))

def load_records():
    """Load records from the CSV file."""
    records = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            records.append((row[0], row[1], row[2]))
    return records

def create_window():
    """Create the main application window."""
    window = tk.Tk()
    window.title("Etkinlik Kaydı")

    entries = [
        ("İsim:", 0, 0),
        ("Soyisim:", 1, 0),
        ("Doğum Tarihi (Gün/Ay/Yıl):", 2, 0)
    ]
    entry_widgets = {}
    for label_text, row, col in entries:
        label = tk.Label(window, text=label_text)
        label.grid(row=row, column=col)
        entry_widgets[label_text] = tk.Entry(window)
        entry_widgets[label_text].grid(row=row, column=col + 1)

    btn_save = tk.Button(window, text="Kaydet", command=lambda: save_entry(
        entry_widgets["İsim:"].get(), entry_widgets["Soyisim:"].get(), entry_widgets["Doğum Tarihi (Gün/Ay/Yıl):"].get(), combo_records))
    btn_save.grid(row=3, columnspan=2)

    lbl_dropdown = tk.Label(window, text="Kayıtlar:")
    lbl_dropdown.grid(row=4, column=0)
    combo_records = ttk.Combobox(window)
    combo_records.grid(row=4, column=1)
    combo_records['values'] = load_records()

    return window

create_csv_file()

if __name__ == "__main__":
    root = create_window()
    root.mainloop()
