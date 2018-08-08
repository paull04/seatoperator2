from random import shuffle
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from os import rename
import os
import gzip
import copy
import pickle
from time import time
import numpy as np

from gstes import GsTes


class Rule:
    @staticmethod
    def no_seat_overlap_rule(pre_name, next_name):
        t = iter(next_name)

        for x in pre_name:
            e = x != next(t)
            print(e)
            yield e

    @staticmethod
    def no_couple_overlap_rule(pre_name, next_name):

        for x in next_name:

            if type(x) != list:
                continue

            d = all([x not in pre_name, list(reversed(x)) not in pre_name])
            print(d)
            yield d


def g_flatten(seat):
    for x in seat:

        if type(x) == list:

            for i in x:
                yield i
        else:
            yield x


def flatten(seat):
    return [x for x in g_flatten(seat)]


def join_seat(seat, part):
    it = iter(part)
    for x in range(len(seat)):
        if type(seat[x]) == list:
            for a in range(len(seat[x])):
                if seat[x][a] in part:
                    seat[x][a] = next(it)
        else:
            if seat[x] in part:
                seat[x] = next(it)


def count_list(ref):
    i = [len(ref) for x in ref if type(ref) == list]
    i.append(len(ref) - len(i))
    return sum(i)


class ChangeSeat:
    @staticmethod
    def change_seat(name_list, couple_ov_op=False, seat_ov_op=False,
                    none_gender=None, boy_seat=None, girl_seat=None):
        try:
            new_name = copy.deepcopy(name_list[-1])

            print(new_name)
            t1 = time()
            while True:
                print(new_name, name_list, none_gender)

                if none_gender:
                    shuffle(none_gender)
                    join_seat(new_name, none_gender)

                    print(new_name)

                if boy_seat:
                    shuffle(boy_seat)
                    join_seat(new_name, boy_seat)

                if girl_seat:
                    shuffle(girl_seat)
                    join_seat(new_name, girl_seat)

                if all([ChangeSeat.rule(pre_seat=x,
                                        next_seat=new_name,
                                        couple_ov_op=couple_ov_op,
                                        seat_ov_op=seat_ov_op) for x in name_list]):
                    print('{}\n{}'.format(name_list, new_name))
                    return flatten(new_name)
                if time() - t1 > 15:
                    raise TimeoutError

        except TimeoutError:
            return 'time error'

        except StopIteration as e:
            return str(e)

    @staticmethod
    def rule(pre_seat, next_seat, couple_ov_op=False, seat_ov_op=False):
        if seat_ov_op:

            for u in Rule.no_seat_overlap_rule(flatten(pre_seat), flatten(next_seat)):

                if not u:
                    return False

        if couple_ov_op:

            for i in Rule.no_couple_overlap_rule(pre_seat, next_seat):

                if not i:
                    return False
        return True


class ExtractName:
    def __init__(self, seat_list=None,
                 couple_ov_op=False,
                 gender_set=False):
        self.seat_list = seat_list
        self.couple_ov_op = couple_ov_op
        self.seat_gender_set = gender_set
        self.name_list = None
        self.boy_name_list = None
        self.girl_name_list = None
        self.none_gender_name_list = None

    def extract_name(self):
        self.name_list = []

        if self.couple_ov_op:
            for x in self.cop():
                if type(x) == list:
                    if list(reversed(x)) in self.name_list:
                        continue
                self.name_list.append(x)
        else:
            self.name_list = [x.name for x in self.seat_list]

        if self.seat_gender_set:
            self.boy_name_list = [x for x in self.gender_extra('boy')]
            self.girl_name_list = [x for x in self.gender_extra('girl')]
            self.none_gender_name_list = [x for x in self.gender_extra('None_gender')]
        else:
            self.none_gender_name_list = flatten(self.name_list)
        return self.name_list, self.none_gender_name_list, self.boy_name_list, self.girl_name_list

    def cop(self):
        for x in self.seat_list:
            if not x.name:
                continue
            if type(x.couple) != type(x):
                yield x.name
                continue
            if not x.couple.name:
                yield x.name
                continue
            yield [x.name, x.couple.name]

    def gender_extra(self, gender=None):
        for x in self.seat_list:
            if x.gender == gender:
                yield x.name


class FileHandler:
    @staticmethod
    def load_file(path='', file_extension=''):
        try:
            if '.' not in path or os.path.splitext(path)[1] != file_extension:
                return False

            with gzip.open(path, 'rb') as f:
                pk = pickle.Unpickler(f)
                file = pk.load()
            return file

        except FileNotFoundError as e:
            return str(e)

    @staticmethod
    def save_file(file, path):
        with gzip.open('temp', 'wb') as f:
            pk = pickle.Pickler(f)
            pk.dump(file)
        rename('temp', path)
        return '저장되었습니다'


COLOR = {
    'boy': 'background-color: blue',
    'girl': 'background-color: pink',
    'None_gender': 'background-color: white'
}
G = {
    'boy': 'girl',
    'girl': 'None_gender',
    'None_gender': 'boy'
}


class Button(QPushButton):

    def __init__(self, name=None, gender=None, couple=None,
                 parent=None, geom=(400, 40), seat=None, lock_bool=False):
        super().__init__(parent=parent)
        if not name:
            name = ''
        if not gender:
            gender = 'None_gender'
        if not couple:
            couple = 'None_couple'

        self.seat = seat
        self.name = name
        self.gender = gender
        self.setStyleSheet(COLOR[gender])
        self.couple = couple
        self.lock_bool = lock_bool
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
        self.couple = "None_gender"

    @QtCore.pyqtSlot()
    def show_txt(self):
        if self.parent().ch_couple:
            self.couple = self.parent().ch_couple
            self.couple.couple = self
            self.parent().ch_couple = None
        name = self.name
        gender = self.gender
        if type(self.couple) == Button:
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

        super(Button, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)

            self.__mouseMovePos = globalPos

        super(Button, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

        super(Button, self).mouseReleaseEvent(event)

    @QtCore.pyqtSlot()
    def del_self(self):
        self.deleteLater()
        self.parent().ch_couple = None
        self.seat.remove(self)

    def save(self):
        if type(self.couple) == str:
            couple = self.couple
        else:
            couple = self.change_couple.name
        return self.name, self.gender, couple, self.dv, self.lock_bool

    def moveEvent(self, a0: QtGui.QMoveEvent):
        self.dv = (self.parent().width() / self.x(),
                   self.parent().height() / self.y())

    def return_x_y(self):
        return self.x(), self.y()

    @property
    def Gender(self):
        return self.gender

    @Gender.setter
    def Gender(self, value):
        self.gender = value
        self.setStyleSheet(COLOR[value])


def change_couple(seat_list, x_y, seat_x_y):
    """
    미완성(자동 짝 바꾸기)
    가까운 자리끼리 짝을 지어주는 함수
    """
    temp = x_y - seat_x_y
    xy = np.array([np.sum(x) for x in temp])
    t = np.delete(xy, 0)
    t = t.min()
    index = np.where(xy == t, xy)
    index2 = np.where(x_y == seat_x_y)
    seat_list[index].couple = seat_list[index2]
    seat_list[index2].couple = seat_list[index]


if __name__ == "__main__":
    g = [['1', '2'], ['3', '4'], ['5', '6']]
    while True:
        b = copy.deepcopy(g)
        a = input()
        if a == 'q':
            exit()
        print(ChangeSeat.change_seat(name_list=b,
                                     seat_ov_op=True,
                                     couple_ov_op=True,
                                     none_gender=flatten(b)))
