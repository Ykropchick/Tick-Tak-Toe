import os
import tkinter as tk
from tkinter import ttk
import subprocess
import re
from game_logic import Main


class StartPage:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Tick-Tak-Toe")
        self.main_window.geometry("600x600")
        self.main_window.configure(bg="gray")
        self.dates = []
        tk.Button(self.main_window, text="Play with friends",
                  command=self.start_game, height=3,
                  width=30, bg="green").place(x=190, y=170)
        tk.Button(self.main_window, text="Load previous games",
                  command=self.load_previous_match, height=3,
                  width=30, bg="green").place(x=190, y=310)
        tk.Button(self.main_window, text="Play with bot",
                  command=self.game_with_bot, height=3,
                  width=30, bg="green").place(x=190, y=240)
        tk.Button(self.main_window, text="See a previous match",
                  command=self.see_previous_match, height=3,
                  width=30, bg="green").place(x=190, y=380)
        self.main_window.mainloop()

    def start_game(self):
        os.system("python game_logic.py off")

    def load_game(self, date):
        os.system(f"python load_previous_match.py {date}")

    def load_previous_match(self):
        self.dates = []
        with open('unfinished_previous_matches') as file:
            for line in file.readlines():
                if line[0:4] == 'date':
                    self.dates.append(str(re.search(r'[1-9](.*)', line)[0]))
        load_window = tk.Tk()
        load_window.geometry("600x600")
        load_window.title("finish_previous_matches")
        load_window.configure(bg="white")
        scroll_window = self.do_scrollbar(load_window)
        for i in range(len(self.dates)):
            tk.Button(scroll_window, text=f'{self.dates[i]}',
                      height=3, width=20,
                      bg="lightgreen", command=lambda i=i: self.load_game(self.dates[i])).grid(column=0, row=i,
                                                                                              sticky="we", padx=220,
                                                                                              pady=5)

    def game_with_bot(self):
        os.system("python game_logic.py on")

    def see_game(self, date):
        os.system(f"python see_previous_match.py {date}")

    def see_previous_match(self):
        self.dates = []
        with open('finish_previous_matches') as file:
            for line in file.readlines():
                if line[0:4] == 'date':
                    self.dates.append(str(re.search(r'[1-9](.*)', line)[0]))
        load_window = tk.Tk()
        load_window.geometry("600x600")
        load_window.title("finish_previous_matches")
        load_window.configure(bg="white")
        scroll_window = self.do_scrollbar(load_window)
        for i in range(len(self.dates)):
            tk.Button(scroll_window, text=f'{self.dates[i]}',
                      height=3, width=20,
                      bg="lightgreen", command=lambda i=i: self.see_game(self.dates[i])).grid(column=0, row=i,
                                                                                              sticky="we", padx=220,
                                                                                              pady=5)
        load_window.mainloop()

    def do_scrollbar(self, window):

        main_frame = tk.Frame(window)
        main_frame.pack(fill=tk.BOTH, expand=1)

        my_canvas = tk.Canvas(main_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
        return second_frame


StartPage()
