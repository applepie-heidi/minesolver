import datetime
import os
import argparse

from keras.models import load_model

import models
from brain import Brain
from difficulty import Difficulty, get_by_name

DEFAULT_SAMPLES = {
    'beginner': 250,
    'intermediate': 1000,
    'expert': 2000,
}

def argggs():
    parser = argparse.ArgumentParser(description='minesolver trainer')
    parser.add_argument(
        '--difficulty', default='beginner', metavar='difficulty',
        help='one of: beginner, intermediate, expert, HxWxM (where H=height, W=width, M=mines)')
    parser.add_argument(
        '--truth', default='predictions', 
        choices=['predictions', 'neighbours', 'board'],
        help='one of: predictions, neighbours, board')
    parser.add_argument(
        '--samples', type=int,
        help='number of game moves for single session')
    args = parser.parse_args()
    return args


def main():

    args = argggs()

    name = 'conv2d_maxpooling_dense_relu_softmax_binarycrosse_adam1'
    difficulty = args.difficulty  # beginner, intermediate, expert, HxWxM
    truth_source = args.truth  # predictions, neighbours, board
    sessions = 100_000
    samples = args.samples
    epochs = 10

    if not samples:
        samples = DEFAULT_SAMPLES.get(args.difficulty)
        if not samples:
            print("you must specify number of samples")
            return

    if difficulty in ('beginner', 'intermediate', 'expert'):
        difi = get_by_name(difficulty)
        model_name = '_'.join([difficulty, name, truth_source])
    else:
        h, w, mines = [int(x) for x in difficulty.split('x')]
        difi = Difficulty(difficulty, dim1_height=h, dim2_width=w, number_of_mines=mines)
        model_name = '_'.join([difficulty, name, truth_source])

    while True:
        choice = int(input('1. Train a new model from scratch \n2. Keep training a pre-trained model\n<1/2>? '))
        if choice == 1:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            model_name = now + '_' + model_name
            log_file = open(f'logs/{model_name}', 'a+')
            make_model = getattr(models, name)
            model = make_model(difi)
            log_file.write(f'DIFFICULTY: {difficulty}\n')
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
            break

        elif choice == 2:
            print('Which one?')
            files = os.listdir('models/')
            filtered_files = []
            i = 0
            for f in files:
                if f.endswith(model_name):
                    filtered_files.append(f)
                    print(f'Choice {i}: {f}')
                    i += 1

            while True:
                file_choice = int(input('Your choice: '))
                try:
                    model_name = filtered_files[file_choice]
                    model = load_model('models/' + model_name)
                    log_file = open(f'logs/{model_name}', 'a+')
                    break
                except IndexError:
                    pass
            break

    brain = Brain(model, difi, model_name, log_file, truth_source)
    brain.learn(samples, sessions, epochs)
    print('finished')

    brain.model.save('models/' + model_name)


if __name__ == '__main__':
    main()
