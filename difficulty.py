# coding: utf-8

class Difficulty:

    def __init__(self, name: str, dim1_height: int, dim2_width: int,
                 number_of_mines: int) -> None:
        self.name = name
        self.dim1_height = dim1_height
        self.dim2_width = dim2_width
        self.number_of_mines = number_of_mines


BEGINNER = Difficulty('beginner', 8, 8, 10)
INTERMEDIATE = Difficulty('intermediate', 16, 16, 40)
EXPERT = Difficulty('expert', 16, 30, 99)

diffs = [BEGINNER, INTERMEDIATE, EXPERT]


def get_by_name(name):
    for d in diffs:
        if d.name == name:
            return d
