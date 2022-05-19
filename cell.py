class Cell:

    def __init__(self, x, y):
        self.mine = False
        self.revealed = False
        self.marked = False
        self.value = 0
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Cell({"*" if self.mine else "-"}/{self.value}, rvl={self.revealed}, mrk={self.marked})'
