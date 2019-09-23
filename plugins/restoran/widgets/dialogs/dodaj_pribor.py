from PySide2 import QtWidgets, QtCore
import csv

class DodajPriborDialog(QtWidgets.QDialog):

    def __init__(self, restoran,parent=None):

        super().__init__(parent)
        self.setWindowTitle("Dodaj pribor u korpu")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
    

        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == restoran:
                   cena =row[7]
        self.labelaCena = QtWidgets.QLabel(self)
        self.labelaCena.setText(cena)
        self.inputKolicina = QtWidgets.QPlainTextEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)
        self.inputKolicina.setPlainText("0")
        self.form_layout.addRow("Cena :", self.labelaCena)
        self.form_layout.addRow("Kolicina :", self.inputKolicina)
        self.labelaCena.setMaximumHeight(20)
        self.inputKolicina.setMaximumHeight(20)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def get_kolicina(self):

        return self.inputKolicina.toPlainText()

    def get_cena(self):

        return self.labelaCena.text()