from keras.models import load_model

from brain_neww import Brain
from game import Game


def test_computer():
    model_name = input("What is the name of the model/model code? ")
    split = model_name.split("_")
    difficulty = split[0]
    name = split[1]
    model = load_model("models/" + model_name)
    brain = Brain(model, difficulty, name)
    games = int(input("How many games to test on? "))
    brain.test(games)


def play_as_a_human():
    difficulty = input("Choose your poison: ")
    while difficulty is not 'beginner' or difficulty is not 'intermediate' or difficulty is not 'expert':
        difficulty = input("I said choose your poison (beginner, intermediate, expert): ")

    game = Game(difficulty)
    print("There are " + str(game.board.number_of_mines) + " total mines.")
    while not game.game_over:
        print(game.board)
        coordinates = input("Enter coordinates: ")
        coordinates = [int(x) for x in coordinates.split(',')]
        if 0 < coordinates[0] <= game.board.board_height and 0 < coordinates[1] <= game.board.board_width:
            coordinates = (coordinates[0] - 1, coordinates[1] - 1)
            game.open_cell(coordinates[0], coordinates[1])
        else:
            print(f"out of bounds, choose ([1, {game.board.board_height}],[1, {game.board.board_width})")
    if game.game_won:
        print(game.board)
        print("I'm on top of the world, HEY!!.")
    else:
        print("It's over isn't it? Isn't it? Isn't it oveeeeer???.")


def play_as_computer():
    model_name = input("What is the name of the model/model code? ")

    split = model_name.split("_")
    difficulty = split[0]
    name = split[1]

    model = load_model("models/" + model_name)

    brain = Brain(model, difficulty, name)
    brain.play()


if __name__ == '__main__':
    test_computer()
