from PySide2 import QtWidgets, QtCore


class PoruciKorpuDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.setWindowTitle("Moja korpa")
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.inputBrTelefona = QtWidgets.QPlainTextEdit(self)
        self.inputAdresa = QtWidgets.QPlainTextEdit(self)
        self.inputNapomena = QtWidgets.QPlainTextEdit(self)
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                                                     | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.form_layout.addRow("Broj telefona :", self.inputBrTelefona)
        self.form_layout.addRow("Adresa dostave :", self.inputAdresa)
        self.form_layout.addRow("Napomena porudzbine :", self.inputNapomena)
        self.inputBrTelefona.setMaximumHeight(20)
        self.inputAdresa.setMaximumHeight(20)
        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)


    def get_brtelefona(self):

        return self.inputBrTelefona.toPlainText()

    def get_adresa(self):

        return self.inputAdresa.toPlainText()

    def get_napomena(self):

        return self.inputNapomena.toPlainText()

    def set_brtelefona(self, brtelefona):

        self.inputBrTelefona.setPlainText(brtelefona)
