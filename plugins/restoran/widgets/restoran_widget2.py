from PySide2 import QtWidgets
from PySide2 import QtGui
from ..restoran_model import RestoranModel
from .porudzbine_restoran_widget import PorudzbineRestoranWidget
from .dialogs.dialog import Dialog
import csv



class RestoranWidget2(QtWidgets.QWidget):

    def __init__(self, name, parent=None):

        super().__init__(parent)
        self._ukupna_cena = 0
        self._name = name
        self._parent = parent
        self.set_layout()

    def set_layout(self):

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.add_jelo = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/hamburger.png"), "Dodaj jelo na meni")
        self.view_porudzbine = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/server.png"), "Primljene porudzbine")
        self.ukloni = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/cross.png"), "Ukloni jelo iz menija")
        self.hbox_layout.addWidget(self.add_jelo)
        self.hbox_layout.addWidget(self.ukloni)
        self.hbox_layout.addWidget(self.view_porudzbine)
        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.add_jelo.clicked.connect(self._on_add_jelo)
        self.ukloni.clicked.connect(self._on_ukloni)
        self.view_porudzbine.clicked.connect(self._on_view_porudzbine)

        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.table_view)


        self.setLayout(self.vbox_layout)
        self._open()

    def set_model(self, model):

        self.table_view.setModel(model)

    def _open(self):

        if(self._name is not None):
            self.set_model(RestoranModel(
                "plugins/restoran/"+self._name+".csv"))

    def _on_add_jelo(self):

        dialog = Dialog().getDodajJeloDialog(self.parent())
        if dialog.exec_() == QtWidgets.QDialog.Accepted:

            naziv = dialog.get_naziv()
            sastojci = dialog.get_sastojci()
            labela = dialog.get_labela()
            cena = dialog.get_cena()
            row =[naziv,sastojci,labela,cena]

            with open("plugins/restoran/"+self._name+".csv", 'r') as readFile:
                reader = csv.reader(readFile)
                lines = list(reader)
                lines.append(row)
            with open("plugins/restoran/"+self._name+".csv", 'w+',newline='') as writeFile:
                writer = csv.writer(writeFile)
                writer.writerows(lines)
            readFile.close()
            writeFile.close()

            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Uspesno je dodato jelo na meni")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()

        self._open()

    def _on_view_porudzbine(self):

        self.unfill(self.vbox_layout)
        PorudzbineRestoranWidget(self._name, self)

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

    def _on_ukloni(self):

        index = sorted(
            set(map(lambda x: x.row(), self.table_view.selectedIndexes())))
        if(len(index) == 0):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedna stavka nije izabrana")
            message.setInformativeText(
                "Izaberite jednu stavku koju zelite da uklonite iz menija")
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

        with open("plugins/restoran/"+self._name+".csv", 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)

        broj = index[0]
        del lines[broj]

        with open("plugins/restoran/"+self._name+".csv", 'w+', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()

        message = QtWidgets.QMessageBox(self.parent())
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setText("Uspesno je uklonjena stavka iz menija")
        message.setWindowTitle("Obavestenje")
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()

        self._open()