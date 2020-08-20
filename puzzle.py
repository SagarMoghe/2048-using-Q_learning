from tkinter import *
from logic import *
import random
import numpy as np
import math
import time
from ai import Dqn

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

brain = Dqn(16, 4, 0.9)
moves = [up, down, right, left]
last_reward = 0
scores = []


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.preprocess()
        self.next_move()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)  # logic function

        self.matrix = add_two(self.matrix)  # logic function
        self.matrix = add_two(self.matrix)  # logic function

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()  # Calls all pending idle tasks, without processing any other events. This can be used to carry out geometry management and redraw widgets if necessary, without calling any callbacks.

    def generate_next(self):
        index = (self.gen(), self.gen())  # Index is a 2 value variable
        while self.matrix[index[0]][index[1]] != 0:  # while matrix @ index 0,1 is not empty
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def preprocess(self):
        self.A = np.hstack(self.matrix)
        self.A1 = [float(i) for i in self.A]
        maxi = max(self.A)
        maxi = math.log(maxi, 2.0)
        for i in range(16):
            if self.A1[i] != 0.0:
                self.A1[i] = math.log(self.A1[i], 2.0) / maxi

    def next_move(self):
        self.last_signal = self.A1
        print(self.last_signal)
        self.last_reward = last_rew()
        print(self.last_reward)
        action = brain.update(self.last_reward, self.last_signal)
        scores.append(brain.score())
        self.matrix, done = moves[action](self.matrix)

        if done:
            self.matrix = add_two(self.matrix)  # logic call
            self.update_grid_cells()
            done = False
            if game_state(self.matrix) == 'win':  # game_state is logic call
                self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
            if game_state(self.matrix) == 'lose':
                self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
        if game_state(self.matrix) == 'not over':
            self.next_move()


gamegrid = GameGrid()
