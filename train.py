import datetime

from keras.models import load_model

from brain import Brain
from difficulty import Difficulty, get_by_name
import models


def main():
    choice = int(input(
        "1. Train a new model from scratch \n2. Keep training a pre-trained model\n<1/2>? "))
    difficulty = 'beginner'
    name = 'conv2d_relu_sigmoid_binarycrosse_adam1'
    truth_source = 'predictions'  # predictions, board, neighbours
    sessions = 100_000  # int(input("How many learning sessions [10000]? "))
    samples = 250  # int(input("How many game moves (clicks) per session [200]? "))
    epochs = 10  # int(input("How many training epochs? "))

    if difficulty != 'custom':
        difi = get_by_name(difficulty)
        model_name = '_'.join([difficulty, name, truth_source])
    else:
        h = 7
        w = 9
        mines = 10
        difficulty = f'{difficulty}{h}x{w}x{mines}'
        difi = Difficulty(difficulty, dim1_height=h, dim2_width=w, number_of_mines=mines)
        model_name = '_'.join([difficulty, name, truth_source])

    if choice == 1:
        make_model = getattr(models, name)
        model = make_model(difi)

    else:
        model = load_model("models/" + model_name)

    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log_file = open(f'logs/{now}_{model_name}', 'w')
    log_file.write(f'DIFFICULLTY: {difficulty}\n')
    log_file.write(f'NAME: {name}\n')
    log_file.write(f'TRUTH ALGORITHM: {truth_source}\n')
    log_file.write(f'SESSIONS: {sessions}\n')
    log_file.write(f'SAMPLES: {samples}\n')
    log_file.write(f'EPOCHS: {epochs}\n')
    log_file.write('\n')
    log_file.write(
        'iteration,loss,val_loss,total_games,total_victories,session_games,session_mean_clicks,'
        'session_mean_victories,session_mean_cells_revealed,session_time\n')
    log_file.flush()

    brain = Brain(model, difi, model_name, log_file, truth_source)
    brain.learn(samples, sessions, epochs)
    print('finished')

    brain.model.save("models/" + model_name)


if __name__ == "__main__":
    main()
