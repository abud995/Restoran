from PySide2 import QtWidgets, QtCore

class DodajJeloDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setWindowTitle("Dodaj jelo na meni")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        

        self.inputNaziv = QtWidgets.QPlainTextEdit(self)
        self.inputSastojci = QtWidgets.QPlainTextEdit(self)
        self.inputLabela = QtWidgets.QPlainTextEdit(self)
        self.inputCena = QtWidgets.QPlainTextEdit(self)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok 
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.form_layout.addRow("Naziv :", self.inputNaziv)
        self.form_layout.addRow("Sastojci :", self.inputSastojci)
        self.form_layout.addRow("Labela (ljuto, popularno itd.) :", self.inputLabela)
        self.form_layout.addRow("Cena :", self.inputCena)


        self.inputNaziv.setMaximumHeight(20)
        self.inputSastojci.setMaximumHeight(20)
        self.inputLabela.setMaximumHeight(20)
        self.inputCena.setMaximumHeight(20)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def get_naziv(self):

        return self.inputNaziv.toPlainText()

    def get_sastojci(self):

        return self.inputSastojci.toPlainText()

    def get_labela(self):

        return self.inputLabela.toPlainText()

    def get_cena(self):

        return self.inputCena.toPlainText()
