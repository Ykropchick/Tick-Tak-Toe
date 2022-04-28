import pygame as pg
from sys import argv
from random import randint
import numpy as np
import time
import re
from game_logic import Main


class SeePreviousMatch(Main):
    def load_game_progress(self):
        name, date1, date2 = argv
        date = date1 + ' ' + date2
        with open("finish_previous_matches", "r") as file:
            s = file.readlines()
            self.loaded_list = []
            flag = False
            for line in s:
                if line[0:4] == 'date':
                    if flag:
                        break
                    if (str(re.search(r'[1-9](.*)', line)[0])) == date:
                        flag = True
                        continue
                if flag:
                    line = line.replace('[', '').replace(']', '').replace('\'', '') \
                        .replace("  ", " ").replace(" x", "x").replace(" o", "o").replace('\n', "")
                    self.loaded_list.append(np.array(line.split(',')).reshape(3, 3))

    def main(self):
        count = 0
        self.load_game_progress()
        self.do_numbering()
        while self.running:
            if count >= len(self.loaded_list):
                self.running = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        self.board_matrix = self.loaded_list[count]
                        count += 1
                    if event.key == pg.K_LEFT and count > 0:
                        count -= 1
                        self.board_matrix = self.loaded_list[count]
            self.do_board()
            self.draw_the_figures()
            pg.display.update()

    def __del__(self):
        pass


ps = SeePreviousMatch()
ps.main()

