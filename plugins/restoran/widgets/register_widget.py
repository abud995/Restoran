from PySide2 import QtWidgets
from PySide2 import QtGui
from ..main_menu_model import MainMenuModel
from .dialogs.dialog import Dialog
from .restoran_widget import RestoranWidget
from .main_menu_widget import MainMenuWidget
import csv


class RegisterWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.set_layout()

    def set_layout(self):

        self.register_user = QtWidgets.QPushButton(
            QtGui.QIcon("resources/icons/disk.png"), "Register", self)

        self.labelaKorime = QtWidgets.QLabel()
        self.labelaKorime.setText("Korisnicko ime :")
        self.inputKorime = QtWidgets.QPlainTextEdit()
        self.labelaLozinka = QtWidgets.QLabel()
        self.labelaLozinka.setText("Lozinka :")
        self.inputLozinka = QtWidgets.QPlainTextEdit()

        self.labelaIme = QtWidgets.QLabel()
        self.labelaIme.setText("Ime :")
        self.inputIme = QtWidgets.QPlainTextEdit()
        self.labelaPrezime = QtWidgets.QLabel()
        self.labelaPrezime.setText("Prezime :")
        self.inputPrezime = QtWidgets.QPlainTextEdit()

        self.labelaBrTelefona = QtWidgets.QLabel()
        self.labelaBrTelefona.setText("Broj telefonaa :")
        self.inputBrTelefona = QtWidgets.QPlainTextEdit()
        self.labelaEmail = QtWidgets.QLabel()
        self.labelaEmail.setText("Email :")
        self.inputEmail = QtWidgets.QPlainTextEdit()

        self.labelaKorime.setMaximumHeight(10)
        self.inputKorime.setMaximumHeight(10)
        self.labelaLozinka.setMaximumHeight(10)
        self.inputLozinka.setMaximumHeight(10)

        self.labelaIme.setMaximumHeight(10)
        self.inputIme.setMaximumHeight(10)
        self.labelaPrezime.setMaximumHeight(10)
        self.inputPrezime.setMaximumHeight(10)

        self.labelaBrTelefona.setMaximumHeight(10)
        self.inputBrTelefona.setMaximumHeight(10)
        self.labelaEmail.setMaximumHeight(10)
        self.inputEmail.setMaximumHeight(10)

        self.inputKorime.setMaximumSize(100, 20)
        self.inputLozinka.setMaximumSize(100, 20)
        self.inputIme.setMaximumSize(100, 20)
        self.inputPrezime.setMaximumSize(100, 20)
        self.inputBrTelefona.setMaximumSize(100, 20)
        self.inputEmail.setMaximumSize(100, 20)

        self.vbox_layout.addWidget(self.labelaKorime)
        self.vbox_layout.addWidget(self.inputKorime)
        self.vbox_layout.addWidget(self.labelaLozinka)
        self.vbox_layout.addWidget(self.inputLozinka)
        self.hbox_layout.addWidget(self.register_user)

        self.vbox_layout.addWidget(self.labelaIme)
        self.vbox_layout.addWidget(self.inputIme)
        self.vbox_layout.addWidget(self.labelaPrezime)
        self.vbox_layout.addWidget(self.inputPrezime)

        self.vbox_layout.addWidget(self.labelaBrTelefona)
        self.vbox_layout.addWidget(self.inputBrTelefona)
        self.vbox_layout.addWidget(self.labelaEmail)
        self.vbox_layout.addWidget(self.inputEmail)

        self.register_user.clicked.connect(self._on_register)

        self.vbox_layout.addLayout(self.hbox_layout)

        self.setLayout(self.vbox_layout)

    def _on_register(self):
        korIme = self.inputKorime.toPlainText()
        lozinka = self.inputLozinka.toPlainText()
        ime = self.inputIme.toPlainText()
        prezime = self.inputPrezime.toPlainText()
        brTelefona = self.inputBrTelefona.toPlainText()
        email = self.inputEmail.toPlainText()
        row = [korIme, lozinka, ime, prezime, brTelefona, email]
       # row2 = None

        if (self.user_found(korIme)):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Korisnicko ime vec postoji")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
        else:
            with open('plugins/restoran/login.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
            with open('plugins/restoran/login.csv', 'w', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close()

            with open("plugins/restoran/Porudzbine"+korIme+".csv", 'w+',newline='') as writeFile:
                writer = csv.writer(writeFile)
               # writer.writerow(row2)
            writeFile.close()

            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Registracija uspesna")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

    def unfill(self, layout):

        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())
        deleteItems(layout)

    def user_found(self, korime):

        with open('plugins/restoran/login.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == korime:
                    return True
        return False
