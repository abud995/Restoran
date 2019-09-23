from PySide2 import QtWidgets
from PySide2 import QtGui
from ..main_menu_model import MainMenuModel
from .dialogs.dialog import Dialog
from .restoran_widget import RestoranWidget
from .main_menu_widget import MainMenuWidget
from .register_widget import RegisterWidget
from .restoran_widget2 import RestoranWidget2
from .register_restoran_widget import RegisterRestoranWidget
import csv


class LoginWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()

        self.set_layout()

    def set_layout(self):

        self.login_user = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/folder-open-document.png"), "Login Korisnik", self)
        self.register_user = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/stickman.png"), "Register Korisnik", self)
        self.login_restoran = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/folder-open-document.png"), "Login Restoran", self)
        self.register_restoran = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/home--plus.png"), "Register Restoran", self)
        self.labelaKorime = QtWidgets.QLabel()
        self.labelaKorime.setText("Korisnicko ime :")
        self.inputKorime = QtWidgets.QPlainTextEdit()
        self.labelaLozinka = QtWidgets.QLabel()
        self.labelaLozinka.setText("Lozinka :")
        self.inputLozinka = QtWidgets.QPlainTextEdit()

        self.labelaKorime.setMaximumHeight(10)
        self.inputKorime.setMaximumHeight(10)
        self.labelaLozinka.setMaximumHeight(10)
        self.inputLozinka.setMaximumHeight(10)

        self.inputKorime.setMaximumSize(100, 20)
        self.inputLozinka.setMaximumSize(100, 20)

        self.labelaKorimeRestoran = QtWidgets.QLabel()
        self.labelaKorimeRestoran.setText("Restoran ime :")
        self.inputKorimeRestoran = QtWidgets.QPlainTextEdit()
        self.labelaLozinkaRestoran = QtWidgets.QLabel()
        self.labelaLozinkaRestoran.setText("Restoran lozinka :")
        self.inputLozinkaRestoran = QtWidgets.QPlainTextEdit()

        self.labelaKorimeRestoran.setMaximumHeight(10)
        self.inputKorimeRestoran.setMaximumHeight(10)
        self.labelaLozinkaRestoran.setMaximumHeight(10)
        self.inputLozinkaRestoran.setMaximumHeight(10)

        self.inputKorimeRestoran.setMaximumSize(100, 20)
        self.inputLozinkaRestoran.setMaximumSize(100, 20)
        self.labelaRazmak = QtWidgets.QLabel()
        self.labelaRazmak.setText("                                   ")
        self.form_layout.addRow(self.labelaKorime, self.inputKorime)
        self.form_layout.addRow(self.labelaLozinka, self.inputLozinka)
        self.form_layout.addRow(self.labelaRazmak,self.labelaRazmak)
        self.form_layout.addRow(self.labelaRazmak,self.labelaRazmak)
        self.form_layout.addRow(
            self.labelaKorimeRestoran, self.inputKorimeRestoran)
        self.form_layout.addRow(
            self.labelaLozinkaRestoran, self.inputLozinkaRestoran)

        self.hbox_layout.addWidget(self.login_user)
        self.hbox_layout.addWidget(self.register_user)
        self.hbox_layout.addWidget(self.login_restoran)
        self.hbox_layout.addWidget(self.register_restoran)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addLayout(self.hbox_layout)

        self.login_user.clicked.connect(self._on_login)
        self.register_user.clicked.connect(self._on_register)
        self.login_restoran.clicked.connect(self._on_login_restoran)
        self.register_restoran.clicked.connect(self._on_register_restoran)

        self.setLayout(self.vbox_layout)

    def _on_login(self):

        korIme = self.inputKorime.toPlainText()
        lozinka = self.inputLozinka.toPlainText()

        if self.user_found(korIme, lozinka):
            filename = "plugins/restoran/Korpa.csv"
            f = open(filename, "w+")
            f.close()
            filename = "plugins/restoran/Pribor.csv"
            f = open(filename, "w+")
            f.close()
            self.wid = MainMenuWidget(korIme)
            self.wid.resize(700, 500)
            self.wid.setWindowTitle('Dobro dosli' + " " + korIme)
            self.wid.show()
        else:
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Pogresno korisnicko ime i/ili lozinka")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

    def _on_register(self):
        self.wid = RegisterWidget()
        self.wid.resize(700, 500)
        self.wid.setWindowTitle('Registracija')
        self.wid.show()

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

    def user_found(self, korime, lozinka):

        with open('plugins/restoran/login.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                try:
                    if row[0] == korime and row[1] == lozinka:
                        return True
                except:

                    return False

    def _on_login_restoran(self):

        korIme = self.inputKorimeRestoran.toPlainText()
        lozinka = self.inputLozinkaRestoran.toPlainText()

        if self.restoran_found(korIme, lozinka):
            # self.unfill(self.vbox_layout)
            # self.unfill(self.hbox_layout)
            self.wid = RestoranWidget2(korIme)
            self.wid.resize(700, 500)
            self.wid.setWindowTitle('Dobro dosli' + " " + korIme)
            self.wid.show()
        else:
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Pogresno korisnicko ime i/ili lozinka")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

    def _on_register_restoran(self):

        self.wid = RegisterRestoranWidget()
        self.wid.resize(700, 500)
        self.wid.setWindowTitle('Registracija')
        self.wid.show()

    def restoran_found(self, korime, lozinka):

        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                try:
                    if row[0] == korime and row[6] == lozinka:
                        return True
                except:

                    return False
