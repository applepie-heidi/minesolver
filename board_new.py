from random import randint

from cell import Cell


class Board:
    def __init__(self, difficulty):
        self.board = None
        self.board_width = None
        self.board_height = None
        self.number_of_mines = None

        if difficulty == 'beginner':
            self.create_board(8, 8, 10)
        elif difficulty == 'intermediate':
            self.create_board(16, 16, 40)
        elif difficulty == 'expert':
            self.create_board(16, 30, 99)
        else:
            raise Exception

    def create_board(self, board_height, board_width, number_of_mines):
        # print('creating board')
        self.board_width = board_width
        self.board_height = board_height
        self.number_of_mines = number_of_mines
        self.board = []  # np.zeroes((board_width, board_height), int)
        for x in range(board_height):
            row = [None] * board_width
            self.board.append(row)
            for y in range(board_width):
                # row.append(Cell(x, y))
                self.set_cell(x, y, Cell(x, y))

    def fill_board(self, x, y):
        # print('fill_board board')
        self.place_mines(x, y)
        self.place_values()

    def place_mines(self, x, y):
        mines_counter = 0

        empty_cell = self.get_cell(x, y)
        neighbours = self.get_neighbours(empty_cell)
        # print(neighbours)

        while mines_counter < self.number_of_mines:
            random_number = randint(0, self.board_height * self.board_width - 1)
            row_count = random_number % self.board_height
            column_count = random_number // self.board_height
            # print(f'placing mine {mines_counter} at {column_count}x{row_count}')
            # print('place m 2', row_count, 'of', self.board_height)
            # print('place m 2', column_count, 'of', self.board_width)
            # print()

            cell = self.get_cell(row_count, column_count)

            if cell is not empty_cell:
                i = 0
                for neighbour in neighbours:
                    if cell is not neighbour:
                        i += 1
                if i == len(neighbours):
                    if not cell.mine:
                        cell.mine = True
                        mines_counter += 1
        print('placed')

    def place_values(self):
        for x in range(self.board_height):
            for y in range(self.board_width):
                # print('place v', x, 'of', self.board_height)
                # print('place v', y, 'of', self.board_width)
                # print()

                cell = self.get_cell(x, y)
                cell_neighbours = self.get_neighbours(cell)
                cell_value = 0
                for cell_neighbour in cell_neighbours:
                    if cell_neighbour.mine:
                        cell_value += 1

                cell.value = cell_value

    def get_neighbours(self, cell):
        x = cell.x
        y = cell.y

        if x == 0:
            if y == 0:
                # print('1')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x+1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y+1, 'of', self.board_width)
                # print()

                neighbours = [self.get_cell(x, y + 1),
                              self.get_cell(x + 1, y + 1),
                              self.get_cell(x + 1, y)]
            elif y == self.board_width - 1:
                # print('2')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x+1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y-1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x + 1, y),
                              self.get_cell(x + 1, y - 1),
                              self.get_cell(x, y - 1)]
            else:
                # print('3')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x+1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y-1, 'of', self.board_width)
                # print('neighbour', y+1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x, y - 1),
                              self.get_cell(x + 1, y - 1),
                              self.get_cell(x + 1, y),
                              self.get_cell(x + 1, y + 1),
                              self.get_cell(x, y + 1)]
        elif x == self.board_height - 1:
            if y == 0:
                # print('4')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x-1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y+1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x - 1, y),
                              self.get_cell(x - 1, y + 1),
                              self.get_cell(x, y + 1)]
            elif y == self.board_width - 1:
                # print('5')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x-1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y-1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x, y - 1),
                              self.get_cell(x - 1, y - 1),
                              self.get_cell(x - 1, y)]
            else:
                # print('6')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x-1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y-1, 'of', self.board_width)
                # print('neighbour', y+1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x, y - 1),
                              self.get_cell(x - 1, y - 1),
                              self.get_cell(x - 1, y),
                              self.get_cell(x - 1, y + 1),
                              self.get_cell(x, y + 1)]
        else:
            if y == 0:
                # print('7')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x-1, 'of', self.board_height)
                # print('neighbour', x+1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y+1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x - 1, y),
                              self.get_cell(x - 1, y + 1),
                              self.get_cell(x, y + 1),
                              self.get_cell(x + 1, y + 1),
                              self.get_cell(x + 1, y)]
            elif y == self.board_width - 1:
                # print('8')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x-1, 'of', self.board_height)
                # print('neighbour', x+1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y-1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x - 1, y),
                              self.get_cell(x - 1, y - 1),
                              self.get_cell(x, y - 1),
                              self.get_cell(x + 1, y - 1),
                              self.get_cell(x + 1, y)]
            else:
                # print('9')
                # print('neighbour', x, 'of', self.board_height)
                # print('neighbour', x-1, 'of', self.board_height)
                # print('neighbour', x+1, 'of', self.board_height)
                # print('neighbour', y, 'of', self.board_width)
                # print('neighbour', y-1, 'of', self.board_width)
                # print('neighbour', y+1, 'of', self.board_width)
                # print()
                neighbours = [self.get_cell(x - 1, y),
                              self.get_cell(x - 1, y - 1),
                              self.get_cell(x, y - 1),
                              self.get_cell(x + 1, y - 1),
                              self.get_cell(x + 1, y),
                              self.get_cell(x + 1, y + 1),
                              self.get_cell(x, y + 1),
                              self.get_cell(x - 1, y + 1)]

        return neighbours

    def open_all_mines(self):
        for row in self.board:
            for cell in row:
                if cell.mine:
                    cell.revealed = True

    def open_cell(self, x, y):
        # print('open cell', x, 'of', self.board_height)
        # print('open cell', y, 'of', self.board_width)
        # print()

        cell = self.get_cell(x, y)
        opened = -1
        if not cell.mine:
            opened = 0
            if not cell.marked and not cell.revealed:
                cell.revealed = True
                opened += 1
                if cell.value == 0:
                    opened += self.open_neighbours(cell)
        return opened

    def open_neighbours(self, cell):
        opened = 0
        neighbours = self.get_neighbours(cell)

        for neighbour in neighbours:
            if not neighbour.revealed and not neighbour.mine and not neighbour.marked:
                neighbour.revealed = True
                opened += 1
                if neighbour.value == 0:
                    opened += self.open_neighbours(neighbour)

        return opened

    def toggle_mark(self, x, y):
        # print('toggle', x, 'of', self.board_height)
        # print('toggle', y, 'of', self.board_width)
        # print()

        cell = self.get_cell(x, y)
        if not cell.revealed:
            cell.marked = not cell.marked

    def set_cell(self, x, y, cell):
        # print('set', y, 'of', self.board_height)
        # print('set', x, 'of', self.board_width)
        # print()
        self.board[x][y] = cell

    def get_cell(self, x, y):
        return self.board[x][y]

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
                if not c.revealed:
                    result += 'X'
                elif c.mine:
                    result += '*'
                else:
                    result += str(c.value)
            result += '\n'

        return result

    def board_str_open(self):
        result = ''

        for row in self.board:
            for c in row:
                if c.mine:
                    result += '*'
                else:
                    result += str(c.value)
            result += '\n'

        return result


if __name__ == '__main__':
    b = Board("beginner")
    print(b)

    b.fill_board(1, 1)
    print(b.board_str())
    print('done?')
    c33 = b.get_cell(3, 3)
    print(f'c33 = {c33}')
