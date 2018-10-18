from os import rename
import os
import gzip
import pickle
from time import time
from random import shuffle

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
import numpy as np

from gstes import GsTes

None_gender = 'None_gender'
boy = 'boy'
girl = 'girl'
None_couple = "None_couple"


class ChangeSeat:
    def __init__(self, seat: list, coup_ov: bool, seat_ov: bool, gen: bool):
        self.gender = {}

        gender = self.gender

        if gen:
            for x in seat:
                gender[boy] = []
                gender[girl] = []
                gender[None_gender] = []
                if x.gender == boy:
                    gender[boy].append(x)
                elif x.gender == girl:
                    gender[girl].append(x)
                else:
                    gender[None_gender].append(x)

            for x in list(gender.keys()):
                if not gender[x]:
                    del gender[x]
        else:
            gender[None_gender] = seat

        for x in gender:
            for y in gender[x]:
                if y.lock_bool:
                    del gender[x][y]

        self._list = {i: [(x.name, x.gender) for x in gender[i]] for i in gender}

        self.rule = []

        if seat_ov:
            self.rule.append(lambda _x, _y: _x.check_new_name(new_name=_y))

        if coup_ov:
            self.rule.append(lambda _x, _y: _x.couple.check_new_couple(new_name=_y)
                             if _x.couple != None_couple else False)

    def __call__(self):
        self.change()
        self.apply()

    def change(self):
        rule = self.rule

        def check(_seat: list, list_: list):
            for func in rule:
                for _x in range(len(list_)):
                    if func(_seat[_x], list_[_x]):
                        return False
            return True

        key = {x: x for x in self.gender}

        while key:
            for x in self._list:
                shuffle(self._list[x])
                print(self._list[x])
                if check(self.gender[x], self._list[x]):
                    del key[x]

    def apply(self):
        for x in self._list:
            for i in range(len(self._list[x])):
                self.gender[x][i].naming(self._list[x][i][0])
                self.gender[x][i].Gender = self._list[x][i][1]


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
