import datetime
import os

from keras.models import load_model

import models
from brain import Brain
from difficulty import Difficulty, get_by_name


def main():
    difficulty = 'beginner'
    name = 'conv2d_relu_sigmoid_binarycrosse_adam1'
    truth_source = 'neighbours'  # predictions, board, neighbours
    sessions = 100_000  # int(input('How many learning sessions [10000]? '))
    samples = 250  # int(input('How many game moves (clicks) per session [200]? '))
    epochs = 10  # int(input('How many training epochs? '))

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

    while True:
        choice = int(input('1. Train a new model from scratch \n2. Keep training a pre-trained model\n<1/2>? '))
        if choice == 1:
            now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            model_name = now + '_' + model_name
            log_file = open(f'logs/{model_name}', 'a+')
            make_model = getattr(models, name)
            model = make_model(difi)
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
            break

        elif choice == 2:
            print('Which one?')
            files = os.listdir('models/')
            filtered_files = []
            i = 1
            for f in files:
                if f.startswith(model_name):
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
