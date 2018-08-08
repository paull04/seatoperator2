from one_dialog import dialog1
from two_dialog import dialog2
import back
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QRect
from PyQt5.QtGui import QCursor, QResizeEvent, QIcon
from mainui import Ui_MainWindow
from sub_dialog import Ui_Dialog
import sys
import numpy as np
from os.path import exists, basename, splitext
import gc
from itertools import chain

try:
    from blist import blist
except ModuleNotFoundError:
    blist = list


class subwidget(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bool = False
        self.buttonBox.accepted.connect(self.change_bool)

    def change_bool(self):
        self.bool = True


def sub(text):
    s = subwidget()
    s.label.setText(text)
    s.exec_()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, seat: blist(), _set: tuple):
        super().__init__()

        self.setupUi(self)
        self.pushButton.setStyleSheet("background-color: green")
        self.setWindowIcon(QIcon('icon.png'))

        self.couple_ov_op = _set[0]
        self.gender_set = _set[1]
        self.seat_ov_op = _set[2]

        self.ch_couple = None
        self.seat = seat
        self.score = 0
        self.history = blist()

        self.setMouseTracking(True)
        self.pushButton_2.clicked.connect(self.add_button)
        self.pushButton.clicked.connect(self.change_seat)
        self.action_create_seat.triggered.connect(self.create_seat)
        self.action_3.triggered.connect(self.user_set)
        self.actionQuit_4.triggered.connect(quit)
        self.actionLoad_file_2.triggered.connect(self.load_file)
        self.actionSave_file_2.triggered.connect(self.save_file)
        self.action_del.triggered.connect(self.del_seat)
        self.action_save_history.triggered.connect(self.save_history)
        self.action_load_history.triggered.connect(self.load_history)

        # self.action_couple.triggered.connect(self.change_couple)
        self.action_give_score.triggered.connect(self.give_score)

    @pyqtSlot()
    def give_score(self):
        score, ok = QInputDialog.getText(self, '점수 주기', '점수')
        if not ok:
            return
        try:
            self.score = int(score)
        except ValueError:
            return

    @pyqtSlot()
    def change_couple(self, seat):
        x_y = np.array([(x.x(), x.y()) for x in seat])
        for x in self.seat:
            back.change_couple(seat_list=self.seat, x_y=x_y, seat_x_y=(x.x(), x.y()))

    @pyqtSlot()
    def del_seat(self):
        for x in self.seat:
            x.deleteLater()
        del self.seat
        self.seat = []
        gc.collect()

    @pyqtSlot()
    def save_history(self):
        f_name = QFileDialog.getSaveFileName(self, caption='history파일 저장하기')
        f_name = f_name[0]
        if f_name == '':
            return
        f = back.FileHandler.save_file(self.history, f_name)
        sub(f)

    @pyqtSlot()
    def load_history(self):
        f_name = QFileDialog.getOpenFileName(self, caption='history파일 불러오기')
        f_name = f_name[0]
        f = back.FileHandler.load_file(f_name, '.history')
        if type(f) == str:
            sub(f)
            return
        elif not f:
            sub('error')
            return
        self.history = f
        print(self.history)

    @pyqtSlot()
    def save_file(self):
        fname = QFileDialog.getSaveFileName(self, caption='저장하기')
        fname = fname[0]
        if not fname:
            return
        t = (self.couple_ov_op, self.gender_set, self.seat_ov_op)
        file = [x.save() for x in self.seat]
        file.append(t)
        file = back.FileHandler.save_file(file, fname)
        del t
        sub(file)

    @pyqtSlot()
    def load_file(self):
        try:
            fname = QFileDialog.getOpenFileName(parent=self)
            fname = fname[0]
            if fname == '':
                return
            file = back.FileHandler.load_file(fname, file_extension='.JARI')
            if file is False:
                sub("잘못된 파일 입니다.")
                return
            if type(file) == str:
                sub(file)
                return
            self.load(file, fname)
        except Exception as e:
            sub(str(e))

    def load(self, file, fname):

        self.couple_ov_op, self.seat_ov_op, self.gender_set = file[-1]
        del file[-1]

        self.ch_couple = None

        print(len(self.seat))
        for x in self.seat:
            x.deleteLater()
        del self.seat
        gc.collect()
        self.seat = blist()
        self.seat.extend([back.Button(x[0], x[1], x[2], self,
                                      (self.width()/x[3][0],
                                       self.height()/x[3][1]),
                                      x[4]) for x in file])
        for x in self.seat:
            for y in self.seat:
                if x.couple == y.name:
                    x.couple = y
            x.show()
        t, _ = splitext(basename(fname))
        self.setWindowTitle(t)

    @pyqtSlot()
    def user_set(self):
        set = dialog2()
        set.exec_()
        self.couple_ov_op, self.seat_ov_op, self.gender_set = set.return_value()

    @pyqtSlot()
    def add_button(self):
        if sys.getsizeof(self.seat) + sys.getsizeof(back.Button) > sys.maxsize:
            sub('리스트가 너무 큽니다.')
            return

        self.seat.append(back.Button(parent=self, seat=self.seat))
        self.seat[-1].show()

    @pyqtSlot()
    def create_seat(self):
        try:
            cr_s=dialog1()
            cr_s.exec_()
            a = cr_s.LIST

            if not a:
                return
            if not a[0][0]:
                n = [str(x) for x in range(1, (int(a[1][1])*int(a[1][0])+1)*2)]
            else:
                n = a[0]
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            n=iter(n)
            y=self.size().height()/(int(a[1][1])+1)
            X=self.size().width()/(int(a[1][0])+1)
            if cr_s.checkBox.isChecked():
                t = [[back.Button(name=next(n), geom=(X*(j+1)-20, y*(i+1)+1), parent=self, seat=self.seat),
                      back.Button(name=next(n), geom=(X*(j+1)+20, y*(i+1)+1), parent=self, seat=self.seat)]
                     for i in range(int(a[1][0])) for j in range(int(a[1][1]))]
                t = list(chain.from_iterable(t))
            else:
                t = [back.Button(name=next(n),
                                 geom=(X*(j+1), y*(i+1)+1),
                                 parent=self,
                                 seat=self.seat)
                     for i in range(int(a[1][1]))
                     for j in range(int(a[1][0]))]

            if cr_s.checkBox_2.isChecked():
                for x, y in enumerate(t):
                     y.Gender = 'boy' if x%2==0 else 'girl'

            for x in t:
                x.show()
            self.seat.extend(t)
            del t

        except OverflowError:
            self.del_seat()
        finally:
            QApplication.restoreOverrideCursor()

    @staticmethod
    def flatten(name_list, filter):
        try:
            name_list.remove(filter)
        except:
            for x in name_list:
                try:
                    if type(x) != list:
                        continue
                    x.remove(filter)
                except:
                    pass

    @pyqtSlot()
    def change_seat(self):
        if not self.seat:
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        lock_list = [x.name for x in self.seat if x.lock_bool]
        print(lock_list)
        extract = back.ExtractName(seat_list=self.seat,
                                   couple_ov_op=self.couple_ov_op,
                                   gender_set=self.gender_set)
        name_list = extract.extract_name()
        print(name_list)
        for x in name_list:
            if not x:
                continue
            for y in lock_list:
                MainWindow.flatten(x, y)

        name_list, none_gender_name_list, boy_name_list, girl_name_list = name_list
        self.history.append(name_list)

        print("전체:{0}\n 무성 : {1}\n 남자 : {2}\n, 여 자 : {3}\n".
              format(name_list, none_gender_name_list, boy_name_list, girl_name_list))
        name_list = back.ChangeSeat.change_seat(name_list = self.history,
                                                couple_ov_op = self.couple_ov_op,
                                                seat_ov_op = self.seat_ov_op,
                                                none_gender = none_gender_name_list,
                                                boy_seat = boy_name_list,
                                                girl_seat = girl_name_list)
        if type(name_list) == str:
            sub(name_list)
            QApplication.restoreOverrideCursor()
            return

        print(name_list)
        it = iter(name_list)
        couple = []
        for w in range(len(name_list)):
            if not self.seat[w].name or self.seat[w].name in couple:
                continue
            self.seat[w].name = next(it)
            self.seat[w].setText(self.seat[w].name)
            if self.couple_ov_op:
                if type(self.seat[w].couple) != str:
                    self.seat[w].couple.name = next(it)
                    self.seat[w].couple.setText(self.seat[w].couple.name)
                    couple.append(self.seat[w].couple.name)
        QApplication.restoreOverrideCursor()

    def resizeEvent(self, a0: QResizeEvent):
        for x in self.seat:
            x.move(self.width()/x.dv[0],
                   self.height()/x.dv[1])
        self.pushButton_2.setGeometry(QRect(int(self.width() * 0.7), 10, 41, 41))
        self.pushButton.setGeometry(QRect(int(self.width() * 0.4), 10, 111, 41))

def main():
    sets = (False, False, False)
    argv = blist()

    try:
        argv = sys.argv[1]
        if exists(argv):
            argv = back.FileHandler.load_file(argv, '.JARI')
            sets = argv[-1]
            argv.extend(argv[:-1])
    except IndexError:
        pass
    finally:
        App = QApplication(sys.argv)
        Main = MainWindow(argv, sets)
        Main.show()
        App.exec_()

if __name__ == "__main__":
    main()
