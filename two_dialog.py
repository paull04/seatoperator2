from PyQt5.QtWidgets import *
from dialog_two import Ui_Set_Seat_Dialog
from PyQt5.QtCore import pyqtSlot
class dialog2(QDialog, Ui_Set_Seat_Dialog):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.couple_overlap = False#True면 짝 중복 제외
        self.seat_overlap = False#True면 자리중복 제외
        self.gender = False#True면 남,여 자리고정
        self.buttonBox.accepted.connect(self.Yes)

    @pyqtSlot()
    def Yes(self):
        self.couple_overlap = self.checkBox.isChecked()
        self.gender = self.checkBox_2.isChecked()
        self.seat_overlap = self.checkBox_3.isChecked()
    def return_value(self):
        return self.couple_overlap, self.seat_overlap, self.gender
if __name__=="__main__":
    import sys
    a=QApplication(sys.argv)
    dlg=dialog2()
    dlg.show()
    a.exec_()
    print(dlg.couple_overlap, dlg.gender, dlg.seat_overlap)