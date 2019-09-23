from PySide2 import QtWidgets
from PySide2 import QtGui
from ..restoran_model import RestoranModel
from .dialogs.dialog import Dialog
import csv
from ..korpa_model import KorpaModel
from .dialogs.poruci_korpu_dialog import PoruciKorpuDialog
import os.path


class KorpaWidget(QtWidgets.QWidget):

    def __init__(self,korime, parent=None):

        super().__init__(parent)
        self.ukupna_cena = 0
        self.korime=korime
        self._parent = parent
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_labele = QtWidgets.QHBoxLayout()
        self.back = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/arrow-curve-180-left.png"), "Nazad")
        self.ukloni = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/cross.png"), "Ukloni iz korpe")
        self.naruci = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/money-bag-dollar.png"), "Poruci korpu", self)
        self.hbox_layout.addWidget(self.back)
        self.hbox_layout.addWidget(self.ukloni)
        self.hbox_layout.addWidget(self.naruci)
        self.table_view = QtWidgets.QTableView(self)
        self.labelaInfo = QtWidgets.QLabel()
        self.labelaInfo.setText("Ukupna cena sa priborom je :")
        self.labelaDostava = QtWidgets.QLabel()
        self.labelaDostava.setText("Dostava restorana :")
        self.labelaCena = QtWidgets.QLabel()
        self._check_pribor()
        self.racunaj_cenu()
        self.cenastr = str(self.ukupna_cena)
        self.labelaCena.setText(self.cenastr)
        self.labelaDostavaCena = QtWidgets.QLabel()
        self.dostava = self._dostava_info()
        self.labelaDostavaCena.setText(self.dostava)
        self.hbox_labele.addWidget(self.labelaInfo)
        self.hbox_labele.addWidget(self.labelaCena)
        self.hbox_labele.addWidget(self.labelaDostava)
        self.hbox_labele.addWidget(self.labelaDostavaCena)


        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

         
        with open("plugins/restoran/Korpa.csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
        readFile.close()

        if not lines:
            self.naruci.setEnabled(False)

        self.back.clicked.connect(self._on_back)
        self.ukloni.clicked.connect(self._on_ukloni)
        self.naruci.clicked.connect(self._on_naruci)

        parent.vbox_layout.addLayout(self.hbox_layout)
        parent.vbox_layout.addWidget(self.table_view)
        parent.vbox_layout.addLayout(self.hbox_labele)

        parent.setLayout(self.vbox_layout)

        self._open()

    def set_model(self, model):

        self.table_view.setModel(model)

    def _open(self):

        self.set_model(KorpaModel("plugins/restoran/Korpa.csv"))

    def _on_naruci(self):

        dialog = Dialog().getPoruciKorpuDialog(self.parent())

        broj = ""

        with open('plugins/restoran/login.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == self.korime:
                    broj = row[4]
        PoruciKorpuDialog.set_brtelefona(dialog,broj)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:

            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Uspesna porudzbina")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()


            brTelefona = dialog.get_brtelefona()
            adresa = dialog.get_adresa()
            napomena = dialog.get_napomena()

            with open('plugins/restoran/Korpa.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                row1 = next(csv_reader)
                restoran = row1[0]

            adresaRestoran = self.dobavi_adresu_restorana(restoran)
            status ="primljena"
            row = [restoran,adresaRestoran,napomena,self.cenastr,adresa,status,self.korime]

            if(os.path.isfile("plugins/restoran/Porudzbine"+self.korime+".csv")):

                with open("plugins/restoran/Porudzbine"+self.korime+".csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
                    lines.append(row)
                with open("plugins/restoran/Porudzbine"+self.korime+".csv", 'w+',newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)
                readFile.close()
                writeFile.close()

            else:
                with open("plugins/restoran/Porudzbine"+self.korime+".csv", 'w+',newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow(row)
                writeFile.close()

            if(os.path.isfile("plugins/restoran/Porudzbine"+restoran+".csv")):

                with open("plugins/restoran/Porudzbine"+restoran+".csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
                    lines.append(row)
                with open("plugins/restoran/Porudzbine"+restoran+".csv", 'w+',newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)
                readFile.close()
                writeFile.close()

            else:
                with open("plugins/restoran/Porudzbine"+restoran+".csv", 'w+',newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerow(row)
                writeFile.close()

            filename = "plugins/restoran/Korpa.csv"
            f = open(filename, "w+")
            f.close()
            filename = "plugins/restoran/Pribor.csv"
            f = open(filename, "w+")
            f.close()


    def _on_back(self):
        
        self._parent.unfill(self._parent.vbox_layout)
        self._parent.set_layout()

    def racunaj_cenu(self):

        with open('plugins/restoran/Korpa.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.ukupna_cena+=int(row[4])

        with open('plugins/restoran/Pribor.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.ukupna_cena+=int(row[0])

    def dobavi_adresu_restorana(self,restoran):

        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == restoran:
                    return row[1]

    def _check_pribor(self):

        with open('plugins/restoran/Korpa.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row1 = next(csv_reader)
            restoran = row1[0]

        with open("plugins/restoran/Pribor.csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
        readFile.close()


        if not lines:
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            message.setText("Niste narucili pribor" + "\n (Narucivanje pribora nije obavezno)")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            dialog = Dialog().getDodajPriborDialog(restoran,self.parent())
            if dialog.exec_() == QtWidgets.QDialog.Accepted:

                cena = int(dialog.get_cena())
                kolicina = int(dialog.get_kolicina())

                priborCena = cena*kolicina
                priborRow = [priborCena]

                with open('plugins/restoran/Pribor.csv', 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
                    lines.append(priborRow)
                with open('plugins/restoran/Pribor.csv', 'w', newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)
                readFile.close()
                writeFile.close()

    def _on_ukloni(self):

        index = sorted(
            set(map(lambda x: x.row(), self.table_view.selectedIndexes())))
        if(len(index) == 0):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedna stavka nije izabrana")
            message.setInformativeText(
                "Izaberite jednu stavku koju zelite da uklonite iz korpe")
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

        with open("plugins/restoran/Korpa.csv", 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)

        broj = index[0]
        del lines[broj]

        with open("plugins/restoran/Korpa.csv", 'w+', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()

        message = QtWidgets.QMessageBox(self.parent())
        message.setIcon(QtWidgets.QMessageBox.Information)
        message.setText("Uspesno je uklonjena stavka iz korpe")
        message.setWindowTitle("Obavestenje")
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.exec_()

        self._open()

    def _dostava_info(self):
        
        dostavaRestorana = ""

        with open('plugins/restoran/Korpa.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row1 = next(csv_reader)
            restoran = row1[0]

        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            reader = csv.reader(csv_file)
            lines = list(reader)

        for row in lines:
            if (row[0] == restoran):
                dostavaRestorana = row[5]


        return dostavaRestorana