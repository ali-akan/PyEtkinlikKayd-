import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

import csv
import os
from datetime import datetime

CSV_FILE = 'katilimcilar.csv'


def create_csv_file():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["İsim", "Soyisim", "Doğum Tarihi"])


def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def is_valid_input(name, surname, dob):
    if not name.strip() or not surname.strip() or not dob.strip():
        raise ValueError("Tüm alanları doldurun!")
    if not is_valid_date(dob):
        raise ValueError("Doğru tarih formatını kullanın (Gün/Ay/Yıl)")


def check_existing_record(name, surname, dob):
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].lower() == name.lower() and row[1].lower() == surname.lower() and row[2] == dob:
                return True
    return False


def save_entry(name, surname, dob, combo_records):
    try:
        is_valid_input(name, surname, dob)

        if check_existing_record(name, surname, dob):
            QMessageBox.information(None, "Bilgi", "Bu kayıt zaten mevcut.")
            return

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, surname, dob])

        QMessageBox.information(None, "Başarılı", "Kayıt başarıyla eklendi!")
        new_record = f"{name}, {surname}, {dob}"

        combo_records.clear()
        combo_records.addItems(load_records())

        index = combo_records.findText(new_record)
        if index != -1:
            combo_records.setCurrentIndex(index)
    except ValueError as e:
        QMessageBox.warning(None, "Hata", str(e))


def load_records():
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
            label_font = QFont('Arial', 12)
            label_font.setBold(True)
            label.setFont(label_font)
            hbox.addWidget(label)
            entry = QLineEdit(default_text, self)
            entry_font = QFont('Arial', 12)
            entry.setFont(entry_font)
            hbox.addWidget(entry)
            vbox.addLayout(hbox)
            self.entry_widgets[label_text] = entry

        self.register_button = QPushButton('Kaydet', self)
        self.register_button.clicked.connect(self.register)
        self.register_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border-radius: 5px;")
        self.register_button.setMinimumHeight(25)
        vbox.addWidget(self.register_button)

        self.dropdown_label = QLabel('Kayıtlar:', self)
        self.dropdown_label_font = QFont('Arial', 12)
        self.dropdown_label_font.setBold(True)
        self.dropdown_label.setFont(self.dropdown_label_font)
        vbox.addWidget(self.dropdown_label)
        self.dropdown_menu = QComboBox(self)
        self.dropdown_menu_font = QFont('Arial', 12)
        self.dropdown_menu.setFont(self.dropdown_menu_font)
        self.dropdown_menu.currentIndexChanged.connect(
            self.display_selected_record)
        vbox.addWidget(self.dropdown_menu)
        self.dropdown_menu.addItems(load_records())

        vbox.addStretch(1)
        self.setLayout(vbox)

    def register(self):
        save_entry(self.entry_widgets["İsim:"].text(), self.entry_widgets["Soyisim:"].text(),
                   self.entry_widgets["Doğum Tarihi (Gün/Ay/Yıl):"].text(), self.dropdown_menu)

    def display_selected_record(self, index):
        if index == -1:
            return
        record = self.dropdown_menu.currentText().split(', ')
        self.entry_widgets["İsim:"].setText(record[0])
        self.entry_widgets["Soyisim:"].setText(record[1])
        self.entry_widgets["Doğum Tarihi (Gün/Ay/Yıl):"].setText(record[2])


def main():
    create_csv_file()
    app = QApplication(sys.argv)
    ex = EventRegistrationApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
