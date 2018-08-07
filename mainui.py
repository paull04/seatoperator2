# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(588, 515)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 10, 40, 40))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 10, 111, 41))
        self.pushButton.setMouseTracking(False)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 588, 28))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuSeat_menu = QtWidgets.QMenu(self.menubar)
        self.menuSeat_menu.setObjectName("menuSeat_menu")
        MainWindow.setMenuBar(self.menubar)
        self.actionFile = QtWidgets.QAction(MainWindow)
        self.actionFile.setObjectName("actionFile")
        self.actionLoad_file_2 = QtWidgets.QAction(MainWindow)
        self.actionLoad_file_2.setObjectName("actionLoad_file_2")
        self.actionSave_file_2 = QtWidgets.QAction(MainWindow)
        self.actionSave_file_2.setObjectName("actionSave_file_2")
        self.action_save_history = QtWidgets.QAction(MainWindow)
        self.action_save_history.setObjectName("action_save_history")
        self.action_load_history = QtWidgets.QAction(MainWindow)
        self.action_load_history.setObjectName("action_load_history")
        self.actionQuit_4 = QtWidgets.QAction(MainWindow)
        self.actionQuit_4.setObjectName("actionQuit_4")
        self.action_create_seat = QtWidgets.QAction(MainWindow)
        self.action_create_seat.setObjectName("action_create_seat")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_del = QtWidgets.QAction(MainWindow)
        self.action_del.setObjectName("action_del")
        self.action_couple = QtWidgets.QAction(MainWindow)
        self.action_couple.setObjectName("action_couple")
        self.action_give_score = QtWidgets.QAction(MainWindow)
        self.action_give_score.setObjectName("action_give_score")

        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionLoad_file_2)
        self.menuMenu.addAction(self.actionSave_file_2)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.action_save_history)
        self.menuMenu.addAction(self.action_load_history)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuit_4)

        self.menuSeat_menu.addSeparator()
        self.menuSeat_menu.addAction(self.action_create_seat)
        self.menuSeat_menu.addSeparator()
        self.menuSeat_menu.addSeparator()
        self.menuSeat_menu.addAction(self.action_3)
        self.menuSeat_menu.addSeparator()
        self.menuSeat_menu.addAction(self.action_del)
        self.menuSeat_menu.addSeparator()
        self.menuSeat_menu.addAction(self.action_couple)
        self.menuSeat_menu.addSeparator()
        self.menuSeat_menu.addAction(self.action_give_score)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuSeat_menu.menuAction())

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "자리바꾸기"))
        self.pushButton.setText(_translate("MainWindow", "교탁"))
        self.menuMenu.setTitle(_translate("MainWindow", "menu"))
        self.menuSeat_menu.setTitle(_translate("MainWindow", "seat menu"))
        self.actionFile.setText(_translate("MainWindow", "file"))
        self.actionLoad_file_2.setText(_translate("MainWindow", "load file"))
        self.actionSave_file_2.setText(_translate("MainWindow", "save file"))
        self.actionQuit_4.setText(_translate("MainWindow", "quit"))
        self.action_create_seat.setText(_translate("MainWindow", "create seat"))
        self.action_3.setText(_translate("MainWindow", "자리 바꾸기 설정"))
        self.action_save_history.setText(_translate("MainWindow", "history파일 저장"))
        self.action_load_history.setText(_translate("MainWindow", "history파일 로드"))
        self.action_del.setText(_translate("MainWindow", "초기화"))
        self.action_couple.setText(_translate("MainWindow", '짝 정하기(미완성)'))
        self.action_give_score.setText(_translate("MainWindow", "점수 주기(미완성)"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

