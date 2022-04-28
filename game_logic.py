import pygame as pg
from sys import argv
from random import randint
import datetime
import re
import numpy as np
import time


class Main:
    def __init__(self):
        pg.init()
        self.Width, self.Height = 800, 800
        self.date = str(re.search(r'^.*\.', str(datetime.datetime.now()))[0])
        self.screen = pg.display.set_mode((self.Width, self.Height))
        self.running = True
        self.numbering = {}
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.size_square = (self.Width // 6, self.Height // 6)
        self.start_pos = (270, 270)
        self.board_matrix = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.pos_square_list = []
        self.surf_square_list = []
        self.figure = "o"
        self.flag_bot = False
        self.reverse_numbering = {}
        self.previous_matrix = [[]]

    def draw_squares(self, x, y):
        square = pg.Surface(self.size_square)
        pos = square.get_rect(center=(x, y))
        square.fill("blue")
        self.pos_square_list.append(pos)
        self.surf_square_list.append(square)
        self.circled_by_lines(square)
        self.screen.blit(square, pos)

    def circled_by_lines(self, surface):
        cord = surface.get_rect()
        pg.draw.line(surface, "white", (cord[0], cord[1]), (cord[0] + cord[2], cord[1]), 3)
        pg.draw.line(surface, "white", (cord[0], cord[1]), (cord[0], cord[1] + cord[3]), 3)
        pg.draw.line(surface, "white", (cord[0] + cord[2], cord[1]), (cord[0] + cord[2], cord[1] + cord[3]), 3)
        pg.draw.line(surface, "white", (cord[0], cord[1] + cord[3]), (cord[0] + cord[2], cord[1] + cord[3]), 3)

    def cross(self, surface):
        pos = surface.get_rect()
        pg.draw.line(surface, "yellow", (pos[0], pos[1]), (pos[2], pos[3]))
        pg.draw.line(surface, "yellow", (pos[0] + pos[2], pos[1]), (pos[0], pos[1] + pos[3]))

    def circle(self, surface):
        pos = surface.get_rect()
        pg.draw.circle(surface, "yellow", (pos[2] // 2, pos[3] // 2), pos[2] // 2, 5)

    def do_numbering(self):
        count = 0
        for i in range(3):
            for j in range(3):
                self.numbering[(i, j)] = count
                count += 1

    def do_reverse_numbering(self):
        count = 0
        for i in range(3):
            for j in range(3):
                self.reverse_numbering[count] = (i, j)
                count += 1

    def draw_the_figures(self):
        for i in range(3):
            for j in range(3):
                if self.board_matrix[j][i] == "o":
                    self.circle(self.surf_square_list[self.numbering[(i, j)]])
                    self.screen.blit(self.surf_square_list[self.numbering[(i, j)]],
                                     self.pos_square_list[self.numbering[(i, j)]])
                elif self.board_matrix[j][i] == "x":
                    self.cross(self.surf_square_list[self.numbering[(i, j)]])
                    self.screen.blit(self.surf_square_list[self.numbering[(i, j)]],
                                     self.pos_square_list[self.numbering[(i, j)]])

    def check_end_game(self):
        if all([" " not in self.board_matrix[i] for i in range(len(self.board_matrix))]):
            self.running = False
        for i in range(3):
            if self.board_matrix[i] == ['o']*3 or self.board_matrix[i] == ['x']*3:
                self.running = False
            if [self.board_matrix[0][i], self.board_matrix[1][i], self.board_matrix[2][i]] == ['o'] * 3 or \
                    [self.board_matrix[0][i], self.board_matrix[1][i], self.board_matrix[2][i]] == ['x'] * 3:
                self.running = False
        if [self.board_matrix[0][0], self.board_matrix[1][1], self.board_matrix[2][2]].count("o") == 3 or \
                [self.board_matrix[0][0], self.board_matrix[1][1], self.board_matrix[2][2]].count("x") == 3:
            self.running = False
        if [self.board_matrix[2][0], self.board_matrix[1][1], self.board_matrix[0][2]].count("o") == 3 or \
                [self.board_matrix[2][0], self.board_matrix[1][1], self.board_matrix[0][2]].count("x") == 3:
            self.running = False

    def do_board(self):
        self.pos_square_list.clear()
        self.surf_square_list.clear()
        self.screen.fill("gray")
        for i in range(3):
            for j in range(3):
                self.draw_squares(self.start_pos[0] + (self.size_square[0]) * i,
                                  self.start_pos[1] + (self.size_square[1]) * j)

    def cursor(self):
        if self.figure == "o":
            pg.draw.circle(self.screen, "green", pg.mouse.get_pos(), 10, 3)
        else:
            pos = pg.mouse.get_pos()
            pg.draw.line(self.screen, "green", (pos[0] - 10, pos[1] - 10), (pos[0] + 10, pos[1] + 10), 3)
            pg.draw.line(self.screen, "green", (pos[0] - 10, pos[1] + 10), (pos[0] + 10, pos[1] - 10), 3)

    def win_lose_template_bot(self, f):
        for i in range(3):
            if self.board_matrix[i].count(f) == 2:
                for j in range(3):
                    if self.board_matrix[i][j] == " ":
                        self.board_matrix[i][j] = "x"
                        self.figure = "o"
                        return True
            if [self.board_matrix[0][i], self.board_matrix[1][i], self.board_matrix[2][i]].count(f) == 2:
                for j in range(3):
                    if self.board_matrix[j][i] == " ":
                        self.board_matrix[j][i] = "x"
                        self.figure = "o"
                        return True

        if [self.board_matrix[0][0], self.board_matrix[1][1], self.board_matrix[2][2]].count(f) == 2:
            if self.board_matrix[0][0] == " ":
                self.board_matrix[0][0] = "x"
                self.figure = "o"
                return True
            if self.board_matrix[1][1] == " ":
                self.board_matrix[1][1] = "x"
                self.figure = "o"
                return True
            if self.board_matrix[2][2] == " ":
                self.board_matrix[2][2] = "x"
                self.figure = "o"
                return True

        if [self.board_matrix[2][0], self.board_matrix[1][1], self.board_matrix[0][2]].count(f) == 2:
            if self.board_matrix[2][0] == " ":
                self.board_matrix[2][0] = "x"
                self.figure = "o"
                return True
            if self.board_matrix[1][1] == " ":
                self.board_matrix[1][1] = "x"
                self.figure = "o"
                return True
            if self.board_matrix[0][2] == " ":
                self.board_matrix[0][2] = "x"
                self.figure = "o"
                return True

    def bot(self):
        if self.win_lose_template_bot("x") or self.win_lose_template_bot("o"):
            return
        i, j = randint(0, 2), randint(0, 2)
        while self.board_matrix[i][j] != " ":
            i, j = randint(0, 2), randint(0, 2)
        self.board_matrix[i][j] = "x"
        self.figure = "o"
        return

    def backup_game(self):
        with open("unfinished_previous_matches", 'a') as file:
            if self.flag_bot == "on":
                file.write(f'date = {self.date}\n' + str(self.board_matrix) + '\non' + f'\n{self.figure}')
            else:
                file.write(f'date = {self.date}\n' + str(self.board_matrix) + '\noff' + f'\n{self.figure}')

    def check_the_start(self):
        name, self.flag_bot = argv

    def upgrade(self):
        self.do_numbering()
        try:
            self.check_the_start()
        except:
            pass
        with open("finish_previous_matches", 'a') as file:
            file.write(f'date = {self.date}\n')
        while self.running:
            self.do_board()
            if self.flag_bot == "on" and self.figure == "x":
                self.bot()
            self.cursor()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.backup_game()
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(len(self.pos_square_list)):
                        if self.pos_square_list[i].collidepoint(pg.mouse.get_pos()):
                            if self.board_matrix[i - (i // 3) * 3][i // 3] == ' ':
                                self.board_matrix[i - (i // 3) * 3][i // 3] = self.figure
                                if self.figure == "o":
                                    self.figure = "x"
                                else:
                                    self.figure = "o"
                    with open("finish_previous_matches", 'a') as file:
                        file.write(str(self.board_matrix) + '\n')
            self.draw_the_figures()
            self.check_end_game()
            self.clock.tick(self.FPS)
            pg.display.update()

    def __del__(self):
        pass
        with open("finish_previous_matches", 'a') as file:
            file.write(f"on {self.figure}")


if __name__ == "__main__":
    main = Main()
    main.upgrade()

