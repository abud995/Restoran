from PySide2 import QtWidgets
from PySide2 import QtGui
from ..main_menu_model import MainMenuModel
from .dialogs.dialog import Dialog
from .restoran_widget import RestoranWidget
from .korpa_widget import KorpaWidget
from .porudzbine_widget import PorudzbineWidget
import csv

class MainMenuWidget(QtWidgets.QWidget):

    def __init__(self, korime, parent=None):

        super().__init__(parent)
        self.korime = korime
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.set_layout()

    def set_layout(self):

        self.open_restoran = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/cake.png"), "Izaberi restoran", self)
        self.open_korpa = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/shopping-basket.png"), "Moja korpa", self)
        self.open_porudzbine = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/address-book-open.png"), "Moje porudzbine", self)
        self.add_restoran = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/gear--plus.png"), "Admin menu (ako bude trebao)", self)
        self.hbox_layout.addWidget(self.open_restoran)
        self.hbox_layout.addWidget(self.open_korpa)
        self.hbox_layout.addWidget(self.open_porudzbine)
        self.hbox_layout.addWidget(self.add_restoran)

        if(self.korime != "Admin"):
            self.add_restoran.setEnabled(False)
            self.add_restoran.setVisible(False)

        with open("plugins/restoran/Korpa.csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
        readFile.close()

        if not lines:
            self.open_korpa.clicked.connect(self._korpa_prazna)
        else:
            self.open_korpa.clicked.connect(self._on_open_korpa)

        with open("plugins/restoran/Porudzbine" + self.korime + ".csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines2 = list(reader)
        readFile.close()

        if not lines2:
            self.open_porudzbine.clicked.connect(self._porudzbine_prazne)
        else:
            self.open_porudzbine.clicked.connect(self._on_open_porudzbine)

        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.open_restoran.clicked.connect(self._on_open_restoran)

        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.table_view)

        self.setLayout(self.vbox_layout)

        self._open()

    def set_model(self, model):

        self.table_view.setModel(model)

    def _open(self):

        self.set_model(MainMenuModel("plugins/restoran/Restorani.csv"))

    def _on_open_restoran(self):

        name = self.table_view.model().open_restoran(self.table_view.selectedIndexes())
        if(name == -1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedan restoran nije izabran")
            message.setInformativeText(
                "Izaberite jedan restoran koji zelite da otvorite")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        elif(name == 1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Izabrano je vise od jednog restorana")
            message.setInformativeText(
                "Izaberite samo jedan restoran koji zelite da otvorite.")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        if(name is not None):
            self.unfill(self.vbox_layout)
            RestoranWidget(name, self)

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

    def _on_open_korpa(self):

        self.unfill(self.vbox_layout)
        KorpaWidget(self.korime, self)

    def _on_open_porudzbine(self):

        self.unfill(self.vbox_layout)
        PorudzbineWidget(self.korime, self)

    def _korpa_prazna(self):

        message = QtWidgets.QMessageBox(self.parent())
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setText("Vasa korpa je prazna")
        message.setWindowTitle("Obavestenje")
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()

    def _porudzbine_prazne(self):

        message = QtWidgets.QMessageBox(self.parent())
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setText("Nemate prethodnih porudzbina")
        message.setWindowTitle("Obavestenje")
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()
