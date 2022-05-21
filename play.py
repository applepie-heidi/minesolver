from keras.models import load_model

from brain import Brain
from difficulty import Difficulty, get_by_name
from game import Game


def play_as_a_human():
    print("Welcome to Minesweeper, fucker.")

    game = Game('beginner')
    message = "Okay, 'Bitch', let's play."
    while not game.game_over:
        print(message)
        print("There are " + str(game.board.number_of_mines) + " total mines.")
        print(game.board)
        message = "You're still alive, somehow."
        coordinates = input("Enter coordinates: ")
        coordinates = [int(x) for x in coordinates.split(',')]
        if 0 < coordinates[0] <= game.board.board_height and 0 < coordinates[1] <= game.board.board_width:
            coordinates = (coordinates[0] - 1, coordinates[1] - 1)
            game.open_cell(coordinates[0], coordinates[1])
        else:
            print("out of bounds")
    if game.game_won:
        print(game.board)
        print("I guess sometimes it's better to be lucky than good. Congratulations.")
    else:
        print("Game over idiot.")


def play_as_computer():
    model_name = input('What is the name of the model? ')
    split = model_name.split('_')
    difficulty = split[1]
    truth_source = split[3]

    difi = get_by_name(difficulty)
    if difi is None:
        h, w, mines = difficulty.split('x')
        h = h[6:]
        difi = Difficulty(difficulty, int(h), int(w), int(mines))

    model = load_model(f'models/{model_name}')
    log_file = open(f'logs')
    brain = Brain(model, difi, model_name, log_file, truth_source)
    brain.play()


if __name__ == '__main__':
    play_as_computer()
