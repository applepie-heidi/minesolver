from random import randint

import numpy as np

from difficulty import Difficulty


class Board:
    def __init__(self, difficulty: Difficulty):
        self.board = np.zeros((difficulty.dim1_height, difficulty.dim2_width, 3))
        self.data = np.zeros((difficulty.dim1_height, difficulty.dim2_width, 11))
        self.difficulty = difficulty
        for y in range(difficulty.dim1_height):
            for x in range(difficulty.dim2_width):
                self.data[y, x, 1] = 1

    @property
    def board_width(self):
        return self.difficulty.dim2_width

    @property
    def board_height(self):
        return self.difficulty.dim1_height

    @property
    def number_of_mines(self):
        return self.difficulty.number_of_mines

    def fill_board(self, y, x):
        self.place_mines(y, x)
        self.place_values()

    def place_mines(self, y, x):
        mines_counter = 0
        neighbours = self.get_neighbours(y, x)

        while mines_counter < self.number_of_mines:
            random_number = randint(0, self.board_height * self.board_width - 1)
            y_mine = random_number // self.board_width
            x_mine = random_number % self.board_width

            if (y, x) != (y_mine, x_mine):
                i = 0
                for neighbour in neighbours:
                    if (y, x) is not neighbour:
                        i += 1
                if i == len(neighbours):
                    if not self.board[y, x, 1]:
                        self.board[y_mine, x_mine, 1] = 1
                        mines_counter += 1

    def place_values(self):
        for x in range(self.board_width):
            for y in range(self.board_height):
                cell_neighbours = self.get_neighbours(y, x)
                cell_value = 0
                for cell_neighbour_y, cell_neighbour_x in cell_neighbours:
                    if self.board[cell_neighbour_y, cell_neighbour_x, 1]:  # is mine
                        cell_value += 1

                self.board[y, x, 2] = cell_value

    def get_neighbours(self, y, x):
        if x == 0:
            if y == 0:
                neighbours = [(y + 1, x),
                              (y + 1, x + 1),
                              (y, x + 1)]
            elif y == self.board_height - 1:
                neighbours = [(y, x + 1),
                              (y - 1, x + 1),
                              (y - 1, x)]
            else:
                neighbours = [(y - 1, x),
                              (y - 1, x + 1),
                              (y, x + 1),
                              (y + 1, x + 1),
                              (y + 1, x)]
        elif x == self.board_width - 1:
            if y == 0:
                neighbours = [(y, x - 1),
                              (y + 1, x - 1),
                              (y + 1, x)]
            elif y == self.board_height - 1:
                neighbours = [(y - 1, x),
                              (y - 1, x - 1),
                              (y, x - 1)]
            else:
                neighbours = [(y - 1, x),
                              (y - 1, x - 1),
                              (y, x - 1),
                              (y + 1, x - 1),
                              (y + 1, x)]
        else:
            if y == 0:
                neighbours = [(y, x - 1),
                              (y + 1, x - 1),
                              (y + 1, x),
                              (y + 1, x + 1),
                              (y, x + 1)]
            elif y == self.board_height - 1:
                neighbours = [(y, x - 1),
                              (y - 1, x - 1),
                              (y - 1, x),
                              (y - 1, x + 1),
                              (y, x + 1)]
            else:
                neighbours = [(y, x - 1),
                              (y - 1, x - 1),
                              (y - 1, x),
                              (y - 1, x + 1),
                              (y, x + 1),
                              (y + 1, x + 1),
                              (y + 1, x),
                              (y + 1, x - 1)]

        return neighbours

    def open_all_mines(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y, x, 1]:
                    self.board[y, x, 0] = 1

    def open_data_cell(self, y, x):
        self.data[y, x, 0] = 1
        value = self.board[y, x, 2]
        self.data[y, x, 2] = 1 if value == 0 else 0
        self.data[y, x, 3] = 1 if value == 1 else 0
        self.data[y, x, 4] = 1 if value == 2 else 0
        self.data[y, x, 5] = 1 if value == 3 else 0
        self.data[y, x, 6] = 1 if value == 4 else 0
        self.data[y, x, 7] = 1 if value == 5 else 0
        self.data[y, x, 8] = 1 if value == 6 else 0
        self.data[y, x, 9] = 1 if value == 7 else 0
        self.data[y, x, 10] = 1 if value == 8 else 0

    def open_cell(self, y, x):
        opened = -1
        if not self.board[y, x, 1]:
            opened = 0
            if not self.board[y, x, 0]:
                self.board[y, x, 0] = 1
                self.open_data_cell(y, x)
                opened += 1
                if self.board[y, x, 2] == 0:
                    opened += self.open_neighbours(y, x)
        return opened

    def open_neighbours(self, y, x):
        opened = 0
        neighbours = self.get_neighbours(y, x)

        for neighbour_y, neighbour_x in neighbours:
            if not self.board[neighbour_y, neighbour_x, 0] and not self.board[neighbour_y, neighbour_x, 1]:
                self.board[neighbour_y, neighbour_x, 0] = 1
                self.open_data_cell(neighbour_y, neighbour_x)

                opened += 1
                if self.board[neighbour_y, neighbour_x, 2] == 0:
                    opened += self.open_neighbours(neighbour_y, neighbour_x)

        return opened

    def get_hidden_cells_near_revealed_cells(self):
        result = set()
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y, x, 0] and not self.board[y, x, 1] and self.board[y, x, 2] != 0:
                    neighbours = self.get_neighbours(y, x)
                    hidden_neighbours = []
                    for n_y, n_x in neighbours:
                        if not self.board[n_y, n_x, 0]:
                            hidden_neighbours.append((n_y, n_x))
                    result.update(hidden_neighbours)
        return result

    def get_dimensions(self):
        return self.board_height, self.board_width

    def get_number_of_mines(self):
        return self.number_of_mines

    def __repr__(self):
        return self.board_str()
        # return f'Board({self.board_width}, {self.board_height})'

    def board_str(self):
        result = ''

        for row in self.board:
            for c in row:
                if not c[0]:
                    result += 'X'
                elif c[1]:
                    result += '*'
                else:
                    result += str(c[2])
            result += '\n'

        return result


if __name__ == '__main__':
    pass
