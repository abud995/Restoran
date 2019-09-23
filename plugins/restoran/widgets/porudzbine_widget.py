from PySide2 import QtWidgets
from PySide2 import QtGui
from ..restoran_model import RestoranModel
from .dialogs.dialog import Dialog
import csv
from ..porudzbine_model import PorudzbineModel
from .dialogs.poruci_korpu_dialog import PoruciKorpuDialog


class PorudzbineWidget(QtWidgets.QWidget):

    def __init__(self, korime, parent=None):

        super().__init__(parent)
        self.ukupna_cena = 0
        self.korime = korime
        self._parent = parent
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_labele = QtWidgets.QHBoxLayout()
        self.back = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/arrow-curve-180-left.png"), "Nazad")
        self.dostavljena = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/mail.png"), "Oznaci porudzbinu kao dostavljenu")
        self.hbox_layout.addWidget(self.back)
        self.hbox_layout.addWidget(self.dostavljena)
        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.back.clicked.connect(self._on_back)
        self.dostavljena.clicked.connect(self._on_dostavljena)

        parent.vbox_layout.addLayout(self.hbox_layout)
        parent.vbox_layout.addWidget(self.table_view)
        parent.vbox_layout.addLayout(self.hbox_labele)

        parent.setLayout(self.vbox_layout)

        self._open()

    def set_model(self, model):

        self.table_view.setModel(model)

    def _open(self):

        self.set_model(PorudzbineModel(
            "plugins/restoran/Porudzbine"+self.korime+".csv"))

    def _on_back(self):

        self._parent.unfill(self._parent.vbox_layout)
        self._parent.set_layout()

    def _on_dostavljena(self):

        index = sorted(
            set(map(lambda x: x.row(), self.table_view.selectedIndexes())))
        if(len(index) == 0):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedna stavka nije izabrana")
            message.setInformativeText(
                "Izaberite jednu stavku koju zelite da oznacite kao dostavljenu")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        elif(len(index) > 1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Izabrano je vise od jedne stavke")
            message.setInformativeText(
                "Mozete izabrati samo jednu stavku")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return

        with open("plugins/restoran/Porudzbine"+self.korime+".csv", 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)

        broj = index[0]
        red = lines[broj]
        red2 = red.copy()

        if red[5] != "prihvacena":
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Pogresan status stavke")
            message.setInformativeText(
                "Samo porudzbinu sa statusom prihvacena mozete oznaciti kao dostavljenu")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

        else:

            red[5] = "dostavljena"
            restoran = red[0]

            del lines[broj]
            lines.insert(broj, red)

            with open("plugins/restoran/Porudzbine"+self.korime+".csv", 'w+', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close()

            with open("plugins/restoran/Porudzbine"+restoran+".csv", 'r') as readFile:
                reader = csv.reader(readFile)
                lines2 = list(reader)

            indeks = -1
            for row in lines2:
                indeks += 1
                if(row == red2):
                    break

            korRed = lines2[indeks]

            korRed[5] = "dostavljena"

            del lines2[indeks]
            lines2.insert(indeks, korRed)

            with open("plugins/restoran/Porudzbine"+restoran+".csv", 'w+', newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines2)
            readFile.close()
            writeFile.close()

            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Porudzbina je oznacena kao dostavljena")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

            self._open()
