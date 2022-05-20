import board as b


class Game:
    def __init__(self, difficulty):
        self.board = b.Board(difficulty)
        self.game_started = False
        self.game_over = False
        self.mines_count = 0
        self.game_won = False
        self.opened_cells = 0
        w, h = self.board.get_dimensions()
        self.cells_count = w * h

    def open_cell(self, x, y):
        w, h = self.board.get_dimensions()
        if 0 <= x < w and 0 <= y < h:
            # print('opening cell: (' + str(x) + ', ' + str(y)+')')

            if not self.game_started:
                self.board.fill_board(x, y)
                self.game_started = True

            opened = self.board.open_cell(x, y)
            if opened == -1:
                self.game_over = True
                self.board.open_all_mines()
            else:
                self.opened_cells += opened

            if self.cells_count - self.opened_cells == self.board.get_number_of_mines():
                self.game_over = True
                self.game_won = True
            return True
        return False


if __name__ == '__main__':
    print('Run as main')
