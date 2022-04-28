import pygame as pg
from game_logic import  Main
from sys import argv
from random import randint
import datetime
import re
import numpy as np
import time



class LoadPreviousMatch(Main):

    def settings(self):
        print(argv)
        name, date1, date2 = argv
        self.date = date1 + ' ' + date2
        self.do_reverse_numbering()
        with open("unfinished_previous_matches", "r") as file:
            s = file.readlines()
            for i in range(len(s)):
                if s[i][0:4] == "date":
                    if str(re.search(r'[1-9](.*)', s[i])[0]) == self.date:
                        self.date = str(re.search(r'[1-9](.*)', s[i])[0])
                        print(s[i+1])
                        self.board_matrix = np.array(s[i+1].replace('[', '').replace(']', '').replace('\'', '') \
                    .replace("  ", " ").replace(" x", "x").replace(" o", "o").replace('\n', "").split(',')).reshape(3, 3)
                        self.board_matrix = list(self.board_matrix)
                        for i in range(len(self.board_matrix)):
                            self.board_matrix[i] = list(self.board_matrix[i])
                        self.flag_bot = s[i+2]
                        self.figure = s[i+3]
                        break


lp = LoadPreviousMatch()
lp.settings()
lp.upgrade()