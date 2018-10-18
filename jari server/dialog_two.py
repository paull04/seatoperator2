# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Set_Seat_Dialog(object):
    def setupUi(self, Set_Seat_Dialog):
        Set_Seat_Dialog.setObjectName("Set_Seat_Dialog")
        Set_Seat_Dialog.resize(402, 280)
        self.buttonBox = QtWidgets.QDialogButtonBox(Set_Seat_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Set_Seat_Dialog)
        self.groupBox.setGeometry(QtCore.QRect(50, 48, 311, 171))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(3, 0, 67, 17))
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(10, 40, 111, 23))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 81, 121, 23))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 122, 121, 23))
        self.checkBox_3.setObjectName("checkBox_3")
        self.label.raise_()
        self.checkBox.raise_()
        self.checkBox.raise_()
        self.checkBox_2.raise_()
        self.checkBox_3.raise_()

        self.retranslateUi(Set_Seat_Dialog)
        self.buttonBox.accepted.connect(Set_Seat_Dialog.accept)
        self.buttonBox.rejected.connect(Set_Seat_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Set_Seat_Dialog)

    def retranslateUi(self, Set_Seat_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Set_Seat_Dialog.setWindowTitle(_translate("Set_Seat_Dialog", "set_seat"))
        self.label.setText(_translate("Set_Seat_Dialog", "선택"))
        self.checkBox.setText(_translate("Set_Seat_Dialog", "짝 중복 제외"))
        self.checkBox_2.setText(_translate("Set_Seat_Dialog", "남·여 자리 고정"))
        self.checkBox_3.setText(_translate("Set_Seat_Dialog", "자리 중복 제외"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Set_Seat_Dialog = QtWidgets.QDialog()
    ui = Ui_Set_Seat_Dialog()
    ui.setupUi(Set_Seat_Dialog)
    Set_Seat_Dialog.show()
    sys.exit(app.exec_())

