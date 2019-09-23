from PySide2 import QtWidgets
from PySide2 import QtGui
from ..restoran_model import RestoranModel
from .dialogs.dialog import Dialog
import csv


class RestoranWidget(QtWidgets.QWidget):

    def __init__(self, name, parent=None):

        super().__init__(parent)
        self._ukupna_cena = 0
        self._name = name
        self._parent = parent
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.back = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/arrow-curve-180-left.png"), "&Nazad")
        self.add_button = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/plus.png"), "&Dodaj u korpu", self)
        self.add_pribor = QtWidgets.QPushButton(QtGui.QIcon(
            "resources/icons/tick-button.png"), "&Dodaj pribor", self)
        self.hbox_layout.addWidget(self.back)
        self.hbox_layout.addWidget(self.add_button)
        self.hbox_layout.addWidget(self.add_pribor)
        self.table_view = QtWidgets.QTableView(self)

        self.table_view.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.back.clicked.connect(self._on_back)
        self.add_button.clicked.connect(self._on_add)
        self.add_pribor.clicked.connect(self._on_add_pribor)

        parent.vbox_layout.addLayout(self.hbox_layout)
        parent.vbox_layout.addWidget(self.table_view)

        parent.setLayout(self.vbox_layout)

        self._open()

    def set_model(self, model):

        self.table_view.setModel(model)

    def _open(self):

        if(self._name is not None):
            self.set_model(RestoranModel(
                "plugins/restoran/"+self._name+".csv"))

    def _on_add(self):

        index = sorted(
            set(map(lambda x: x.row(), self.table_view.selectedIndexes())))
        if(len(index) == 0):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Nijedna stavka nije izabrana")
            message.setInformativeText(
                "Izaberite jednu stavku koju zelite da dodate u korpu")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        elif(len(index) > 1):
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Critical)
            message.setText("Izabrano je vise od jedne stavke")
            message.setInformativeText(
                "Izaberite samo jednu stavku koju zelite da dodate u korpu")
            message.setWindowTitle("Greska")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            return
        dialog = Dialog().getDodajUKorpuDialog(self.parent())
        if dialog.exec_() == QtWidgets.QDialog.Accepted:

            kolicina = dialog.get_kolicina()
            napomena = dialog.get_napomena()
            indeks = index[0]

            hrana = self.table_view.model().get_data()
            hrana2 = hrana[indeks]
            cena = hrana2[3]
            ime = hrana2[0]
            int_kolicina = int(kolicina)
            int_cena = int(cena)
            ukupnaCena = int_cena*int_kolicina
            dostava = ""
            drugiRestoran = False

            with open("plugins/restoran/Korpa.csv", 'r') as readFile:
                        reader = csv.reader(readFile)
                        lines = list(reader)
            readFile.close()

            if not lines:
                
                self.dodaj_u_korpu(ime, kolicina, napomena, ukupnaCena, dostava)
            else:
                if(self.isti_restoran()):
                    self.dodaj_u_korpu(ime, kolicina, napomena, ukupnaCena, dostava)
                else:
                    filename = "plugins/restoran/Pribor.csv"
                    f = open(filename, "w+")
                    f.close()
                    self.dodaj_novo_obrisi_staro(ime, kolicina, napomena, ukupnaCena, dostava)
                    drugiRestoran = True

            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Information)
            if(drugiRestoran):
                message.setText("Uspesno je dodata stavka u korpu" + "\n"+"\n U korpi mogu da se nalaze samo jela iz istog restorana, sve stavke iz drugih restorana su obrisane iz korpe (ukljucujuci i pribor)")
            else:
                message.setText("Uspesno je dodata stavka u korpu")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
            

    def _on_back(self):

        self._parent.unfill(self._parent.vbox_layout)
        self._parent.set_layout()

    def _on_add_pribor(self):


        with open("plugins/restoran/Korpa.csv", 'r') as readFile:
                    reader = csv.reader(readFile)
                    lines = list(reader)
        readFile.close()

        if not lines:
            
            message = QtWidgets.QMessageBox(self.parent())
            message.setIcon(QtWidgets.QMessageBox.Warning)
            message.setText("Ne mozete dodati pribor u praznu korpu")
            message.setWindowTitle("Obavestenje")
            message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            message.exec_()
        else:
            dialog = Dialog().getDodajPriborDialog(self._name,self.parent())
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

                message = QtWidgets.QMessageBox(self.parent())
                message.setIcon(QtWidgets.QMessageBox.Information)
                message.setText("Uspesno je dodat pribor")
                message.setWindowTitle("Obavestenje")
                message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message.exec_()

    def dodaj_u_korpu(self, ime, kolicina, napomena, ukupnaCena, dostava):
        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == self._name:
                    dostava = row[5]

        row = [self._name, ime, kolicina, napomena, ukupnaCena, dostava]

        with open('plugins/restoran/Korpa.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            lines = list(reader)
            lines.append(row)
        with open('plugins/restoran/Korpa.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        readFile.close()
        writeFile.close()

    def isti_restoran(self):

        with open('plugins/restoran/Korpa.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == self._name:
                    return True
                    break
        return False

    def dodaj_novo_obrisi_staro(self, ime, kolicina, napomena, ukupnaCena, dostava):
        with open('plugins/restoran/Restorani.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if row[0] == self._name:
                    dostava = row[5]

        row = [self._name, ime, kolicina, napomena, ukupnaCena, dostava]

        with open('plugins/restoran/Korpa.csv', 'w+', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(row)
        writeFile.close()

