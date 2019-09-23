from PySide2 import QtCore
from .restoran_model import RestoranModel
import csv
import os


class MainMenuModel(QtCore.QAbstractTableModel):

    def __init__(self, path=""):

        super().__init__()
        self._data = []
        self.load_data(path)

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):

        return 6

    def data(self, index, role):

        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):

        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "Naziv"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Adresa"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Broj telefona"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "Vreme cekanja"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return "Min za dostavu"
            elif (section == 5) and (role == QtCore.Qt.DisplayRole):
                return "Tip dostave"

    def setData(self, index, value, role):

        try:
            if value == "":
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged()
            return True
        except:
            return False

    def get_element(self, index: QtCore.QModelIndex):

        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def load_data(self, path=""):

        with open(path, "r", encoding="utf-8") as fp:
            self._data = list(csv.reader(fp, dialect=csv.unix_dialect))

    def open_restoran(self, indices):
        
        indices = sorted(set(map(lambda x: x.row(), indices)))
        if(len(indices)==0):
            return -1
        elif(len(indices)>1):
            return 1
        name = self._data[indices[0]][0]
        return name
