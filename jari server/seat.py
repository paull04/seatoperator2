from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui

from back import None_gender, boy, girl, None_couple
from gstes import GsTes

COLOR = {
    boy: 'border:5px solid blue',
    girl: 'border:5px solid pink',
    None_gender: 'border:5px solid Black'
}
G = {
    boy: girl,
    girl: None_gender,
    None_gender: boy
}


class Seat(QPushButton):

    def __init__(self, name='', gender=None_gender, couple=None_couple,
                 parent=None, geom=(400, 40), seat=[],
                 lock_bool=False, seat_h=None, couple_h=None):
        super().__init__(parent=parent)

        self.seat = seat
        self.name = name
        self.seat_h = seat_h
        self.gender = gender
        self.setStyleSheet(COLOR[gender])
        self.couple = couple
        self.couple_h = couple_h
        self.lock_bool = lock_bool

        self.__mousePressPos = None
        self.__mouseMovePos = None

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)
        self.popMenu = QMenu(self)
        self.popMenu.addSeparator()
        self.popMenu.addAction('삭제하기', self.del_self)
        self.popMenu.addSeparator()
        self.popMenu.addAction('짝 바꾸기', self.change_couple)
        self.popMenu.addSeparator()
        self.popMenu.addAction('이름 바꾸기', self.change_name)
        self.popMenu.addSeparator()
        self.popMenu.addAction('고정', self.lock)
        self.popMenu.addSeparator()
        self.popMenu.addAction('점수 주기', self.give_score)
        self.popMenu.addSeparator()

        self.setText(self.name)

        self.setGeometry(QtCore.QRect(geom[0], geom[1], 40, 40))
        self.setText(self.name)
        self.clicked.connect(self.show_txt)

        self.dv = (
            Seat.f_(self.parent().width(), self.x()),
            Seat.f_(self.parent().height(), self.y())
       )

        self.show()

    @staticmethod
    def f_(width: int, x: int):
        try:
            return x / width
        except ZeroDivisionError:
            return 0

    def set_xy(self):
        self.dv = ()

    def naming(self, value):
        self.name = value
        self.setText(value)

    def check_new_name(self, new_name)->bool:
        if self.seat_h:
            a = new_name in self.seat_h
            print(self.seat_h, a, new_name)
            return a
        return False

    def check_new_couple(self, new_couple)->bool:
        if self.couple_h:
            return new_couple in self.couple_h
        return False

    def append_coup_and_master(self):
        temp = (self.name, self.gender)

        if self.seat_h:
            if temp not in self.seat_h:
                self.seat_h.append(temp)
        else:
            self.seat_h = [temp]

        if self.couple != None_couple:
            temp = (self.couple.name, self.couple.gender)
            if self.couple_h:
                if temp in self.couple_h:
                    self.couple_h.append(temp)
            else:
                self.couple_h = [temp]

    def on_context_menu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))

    @QtCore.pyqtSlot()
    def give_score(self):
        widget = GsTes()
        widget.exec_()

    @QtCore.pyqtSlot()
    def lock(self):
        self.lock_bool = False if self.lock_bool else True
        self.couple.couple = None
        self.couple = None_couple

    @QtCore.pyqtSlot()
    def show_txt(self):
        if self.parent().ch_couple:
            self.couple = self.parent().ch_couple
            self.couple.couple = self
            self.parent().ch_couple = None
        name = self.name
        gender = self.gender

        if self.couple != None_couple:
            couple_name = self.couple.name

        else:
            couple_name = self.couple

        txt = '이름: {0}, 성별: {1},  짝: {2}, 고정 여부: {3}'.format(name, gender, couple_name, self.lock_bool)
        self.parent().statusbar.showMessage(txt)

    @QtCore.pyqtSlot()
    def change_couple(self):
        self.parent().ch_couple = self

    @QtCore.pyqtSlot()
    def change_name(self):
        name, ok = QInputDialog.getText(self, '이름 바꾸기', '이름')
        if not ok:
            return
        self.name = name
        self.setText(self.name)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        self.change_gender()

    def change_gender(self):
        self.gender = G[self.gender]
        self.setStyleSheet(COLOR[self.gender])

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(Seat, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.dv = (Seat.f_(self.parent().width(), self.x()),
                       Seat.f_(self.parent().height(), self.y()))

            self.__mouseMovePos = globalPos

        super(Seat, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(Seat, self).mouseReleaseEvent(event)

    @QtCore.pyqtSlot()
    def del_self(self):
        self.deleteLater()
        self.parent().ch_couple = None
        self.seat.remove(self)

    def save(self):
        if self.couple != None_couple:
            couple = self.seat.index(self.couple)
        else:
            couple = self.couple
        return self.name, self.gender, couple, self.dv, self.lock_bool, self.seat_h, self.couple_h

    def return_x_y(self):
        return self.x(), self.y()

    @property
    def Gender(self):
        return self.gender

    @Gender.setter
    def Gender(self, value):
        self.gender = value
        self.setStyleSheet(COLOR[value])