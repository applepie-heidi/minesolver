from keras.models import load_model

from brain import Brain
from difficulty import Difficulty, get_by_name


def main():
    model_name = input('What is the name of the model? ')
    split = model_name.split('_')
    difficulty = split[1]
    truth_source = split[3]

    difi = get_by_name(difficulty)
    if difi is None:
        h, w, mines = difficulty.split('x')
        difi = Difficulty(difficulty, int(h), int(w), int(mines))

    model = load_model(f'models/{model_name}')
    log_file = open(f'logs')
    brain = Brain(model, difi, model_name, log_file, truth_source)
    game_count = int(input('How many games to test on? '))
    brain.test(game_count)


if __name__ == '__main__':
    main()
