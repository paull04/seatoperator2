from PyQt5.QtWidgets import *
from ones_dialog import Ui_Dialog
from PyQt5.QtCore import pyqtSlot
class dialog1(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.student=''
        self.LIST=None
        self.buttonBox.accepted.connect(self.Yes)

    @pyqtSlot()
    def Yes(self):
        self.student=self.plainTextEdit.toPlainText()
        y=self.lineEdit_2.text()
        x=self.lineEdit.text()
        self.x_shape = x if x else 0
        self.y_shape = y if y else 0
        self.LIST = self.return_value()
    def return_value(self):
        self.temp = ''
        self.name_list=[]
        self.student.replace(' ', '')
        self.student.replace('/n', '')
        for x in self.student:
            if x==',':
                if  self.temp not in self.name_list:
                    self.name_list.append(self.temp)
                    self.temp=''
            else:
                self.temp=self.temp + x
        self.name_list.append(self.temp)
        self.t=(self.x_shape, self.y_shape)
        return (self.name_list, self.t)


if __name__ =="__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = dialog1()
    dlg.show()
    app.exec_()
    print(dlg.return_value())