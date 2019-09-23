from .dodaj_u_korpu_dialog import DodajUKorpuDialog
from .poruci_korpu_dialog import PoruciKorpuDialog
from .dodaj_pribor import DodajPriborDialog
from .dodaj_jelo import DodajJeloDialog
from .odbij_dialog import OdbijDialog


class Dialog():

    def __init__(self):
        ""

    def getDodajUKorpuDialog(self, parent):

        return DodajUKorpuDialog(parent)

    def getPoruciKorpuDialog(self, parent):

        return PoruciKorpuDialog(parent)

    def getDodajPriborDialog(self,name, parent):

        return DodajPriborDialog(name,parent)

    def getDodajJeloDialog(self, parent):

        return DodajJeloDialog(parent)

    def getOdbiijDialog(self,parent):
        
        return OdbijDialog(parent)
