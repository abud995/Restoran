from PySide2 import QtWidgets
from PySide2 import QtGui
from ..main_menu_model import MainMenuModel
from .dialogs.dialog import Dialog
from .restoran_widget import RestoranWidget
from .main_menu_widget import MainMenuWidget
import csv


class RegisterRestoranWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.set_layout()

    def set_layout(self):

        self.register_user = QtWidgets.QPushButton(
            QtGui.QIcon("resources/icons/disk.png"), "Register", self)

        self.labelaKorime = QtWidgets.QLabel()
        self.labelaKorime.setText("Ime restorana:")
        self.inputKorime = QtWidgets.QPlainTextEdit()
        self.labelaLozinka = QtWidgets.QLabel()
        self.labelaLozinka.setText("Lozinka :")
        self.inputLozinka = QtWidgets.QPlainTextEdit()

        self.labelaAdresa = QtWidgets.QLabel()
        self.labelaAdresa.setText("Adresa :")
        self.inputAdresa = QtWidgets.QPlainTextEdit()
        self.labelaVreme = QtWidgets.QLabel()
        self.labelaVreme.setText("Prosecno vreme cekanja :")
        self.inputVreme = QtWidgets.QPlainTextEdit()

        self.labelaBrTelefona = QtWidgets.QLabel()
        self.labelaBrTelefona.setText("Broj telefona :")
        self.inputBrTelefona = QtWidgets.QPlainTextEdit()
        self.labelaMinIznos = QtWidgets.QLabel()
        self.labelaMinIznos.setText("Minimalni iznos za dostavu :")
        self.inputMinIznos = QtWidgets.QPlainTextEdit()

        self.labelaTip = QtWidgets.QLabel()
        self.labelaTip.setText("Tip dostave :")
        self.inputTip = QtWidgets.QPlainTextEdit()

        self.labelaPribor = QtWidgets.QLabel()
        self.labelaPribor.setText("Cena pribora :")
        self.inputPribor = QtWidgets.QPlainTextEdit()

        self.labelaKorime.setMaximumHeight(15)
        self.inputKorime.setMaximumHeight(15)
        self.labelaLozinka.setMaximumHeight(15)
        self.inputLozinka.setMaximumHeight(15)

        self.labelaAdresa.setMaximumHeight(15)
        self.inputAdresa.setMaximumHeight(15)
        self.labelaVreme.setMaximumHeight(15)
        self.inputVreme.setMaximumHeight(15)

        self.labelaBrTelefona.setMaximumHeight(15)
        self.inputBrTelefona.setMaximumHeight(15)
        self.labelaMinIznos.setMaximumHeight(15)
        self.inputMinIznos.setMaximumHeight(15)
        self.labelaTip.setMaximumHeight(15)
        self.inputTip.setMaximumHeight(15)
        self.labelaPribor.setMaximumHeight(15)
        self.inputPribor.setMaximumHeight(15)

        self.inputKorime.setMaximumSize(150, 20)
        self.inputLozinka.setMaximumSize(150, 20)
        self.inputAdresa.setMaximumSize(150, 20)
        self.inputVreme.setMaximumSize(150, 20)
        self.inputBrTelefona.setMaximumSize(150, 20)
        self.inputMinIznos.setMaximumSize(150, 20)
        self.inputTip.setMaximumSize(150, 20)
        self.inputPribor.setMaximumSize(150, 20)

        self.vbox_layout.addWidget(self.labelaKorime)
        self.vbox_layout.addWidget(self.inputKorime)
        self.vbox_layout.addWidget(self.labelaLozinka)
        self.vbox_layout.addWidget(self.inputLozinka)
        self.hbox_layout.addWidget(self.register_user)

        self.vbox_layout.addWidget(self.labelaAdresa)
        self.vbox_layout.addWidget(self.inputAdresa)
        self.vbox_layout.addWidget(self.labelaVreme)
        self.vbox_layout.addWidget(self.inputVreme)

        self.vbox_layout.addWidget(self.labelaBrTelefona)
        self.vbox_layout.addWidget(self.inputBrTelefona)
        self.vbox_layout.addWidget(self.labelaTip)
        self.vbox_layout.addWidget(self.inputTip)
        self.vbox_layout.addWidget(self.labelaMinIznos)
        self.vbox_layout.addWidget(self.inputMinIznos)
        self.vbox_layout.addWidget(self.labelaPribor)
        self.vbox_layout.addWidget(self.inputPribor)

        self.register_user.clicked.connect(self._on_register)

        self.vbox_layout.addLayout(self.hbox_layout)

        self.setLayout(self.vbox_layout)

    def _on_register(self):

        korIme = self.inputKorime.toPlainText()
        lozinka = self.inputLozinka.toPlainText()
        adresa = self.inputAdresa.toPlainText()
        vreme = self.inputVreme.toPlainText()
        brTelefona = self.inputBrTelefona.toPlainText()
        minIznos = self.inputMinIznos.toPlainText()
        tip = self.inputTip.toPlainText()
        pribor = self.inputPribor.toPlainText()
        row = [korIme, adresa, brTelefona, vreme, minIznos, tip, lozinka,pribor]

        if (self.user_found(korIme)):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Restoran sa tim imenom je vec registrovan")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
        else:
            with open('plugins/restoran/Restorani.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
            with open('plugins/restoran/Restorani.csv', 'w', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close()

            with open("plugins/restoran/"+korIme+".csv", 'w+', newline='') as writeFile:
                writer = csv.writer(writeFile)
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

        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == korime:
                    return True
        return False
