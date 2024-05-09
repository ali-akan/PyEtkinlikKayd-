import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt
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
            QMessageBox.information(None, "Bilgi", "Bu kayıt zaten mevcut.")
            return

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, surname, dob])

        QMessageBox.information(None, "Başarılı", "Kayıt başarıyla eklendi!")
        combo_records.clear()
        combo_records.addItems(load_records())
    except ValueError as e:
        QMessageBox.warning(None, "Hata", str(e))

def load_records():
    """Load records from the CSV file."""
    records = []
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            records.append(', '.join(row))
    return records

class EventRegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Etkinlik Kaydı')
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(400, 200)  
        self.setStyleSheet("background-color: #f0f0f0;")

        vbox = QVBoxLayout(self)

        entries = [
            ("İsim:", ""),
            ("Soyisim:", ""),
            ("Doğum Tarihi (Gün/Ay/Yıl):", "")
        ]
        self.entry_widgets = {}
        for label_text, default_text in entries:
            hbox = QHBoxLayout()
            label = QLabel(label_text, self)
            label.setFont(QFont('Arial', 12))
            hbox.addWidget(label)
            entry = QLineEdit(default_text, self)
            entry.setStyleSheet("background-color: white; color: black;")
            hbox.addWidget(entry)
            vbox.addLayout(hbox)
            self.entry_widgets[label_text] = entry

        self.register_button = QPushButton('Kaydet', self)
        self.register_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; height: 25px;")
        self.register_button.clicked.connect(self.register)
        vbox.addWidget(self.register_button)

        self.dropdown_label = QLabel('Kayıtlar:', self)
        self.dropdown_label.setFont(QFont('Arial', 12))
        vbox.addWidget(self.dropdown_label)
        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu.setStyleSheet(
            """
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #4CAF50;
                padding: 5px;
                border-radius: 5px;
                min-width: 10em;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: right center;
                width: 20px;
               
            }
            """
        )
        vbox.addWidget(self.dropdown_menu)
        self.dropdown_menu.addItems(load_records())

        vbox.addStretch(1)  
        self.setLayout(vbox)

    def register(self):
        """Handler for registration button click."""
        save_entry(self.entry_widgets["İsim:"].text(), self.entry_widgets["Soyisim:"].text(),
                   self.entry_widgets["Doğum Tarihi (Gün/Ay/Yıl):"].text(), self.dropdown_menu)

def main():
    create_csv_file()
    app = QApplication(sys.argv)
    ex = EventRegistrationApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()