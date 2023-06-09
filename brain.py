import time
from random import randint

import numpy as np
from tensorflow.keras.callbacks import TensorBoard

from board import Board
from game import Game
from models import ModelAdapter


def flipped_revealed(np_board):
    dim1, dim2 = np_board.shape[0:2]
    return np.ones((dim1, dim2, 1)) - np_board[:, :, 0:1]


def get_layer(np_board, lay):
    return np_board[:, :, lay]


def conv_board(samples, samples_index, fit_data, board: Board):
    if fit_data is None:
        x_data = np.zeros((samples, board.difficulty.dim1_height, board.difficulty.dim2_width, 11))
        x2_data = np.zeros((samples, board.difficulty.dim1_height, board.difficulty.dim2_width, 1))
        fit_data = [x_data, x2_data]
    x_data = fit_data[0]
    x2_data = fit_data[1]

    x_new = board.data
    x_data[samples_index] = x_new
    # flip

    x2_new = flipped_revealed(x_new)
    x2_data[samples_index] = x2_new
    predict_input = [np.array([x_new]), np.array([x2_new])]
    return fit_data, predict_input

    # [x_data, x2_data]


class Brain:
    def __init__(self, model, difficulty, name, log_file, truth_source, board_adapter: ModelAdapter):
        self.model = model
        self.difficulty = difficulty
        self.name = name
        self.truth_func = getattr(self, 'get_truth_from_' + truth_source, self.get_truth_from_predictions)
        self.log_file = log_file
        self.model_adapter = board_adapter

    def learn(self, samples, sessions, epochs):
        dim1_h, dim2_w = self.difficulty.dim1_height, self.difficulty.dim2_width
        # x_data = np.zeros((samples, dim1_h, dim2_w, 11))
        # x2_data = np.zeros((samples, dim1_h, dim2_w, 1))
        # y_data = np.zeros((samples, dim1_h, dim2_w, 1))
        self.model_adapter.adapt(self.model, self.difficulty, samples)

        tensorboard = TensorBoard(log_dir=f'tensor_logs/{self.name}')

        total_games_count = 0
        total_victories = 0
        for i in range(sessions):
            started_at = time.time()
            print(f'== Session: {i}')
            victories = 0
            revealed_cells = 0
            clicks = 0
            samples_index = 0
            games_count = 0
            while samples_index < samples:
                game = Game(self.difficulty)
                game.open_cell(randint(0, dim1_h - 1), randint(0, dim2_w - 1))
                game_clicks = 0
                while not game.game_over and samples_index < samples:

                    # predict_input = self.board_adapter.get_predict_input(game.board, samples_index)
                    # convo_func
                    ## x_new = game.board.data
                    ## x_data[samples_index] = x_new
                    ## # flip
                    ## x2_new = flipped_revealed(x_new)
                    ## x2_data[samples_index] = x2_new
                    ## return [np.array([x_new]), np.array([x2_new])]

                    # out = self.model.predict(predict_input)
                    # [np.array([x_new]), np.array([x2_new])])

                    # mine_prob = out.flatten() + get_layer(game.board.board, 0).flatten()
                    # index_not_a_mine = np.argmin(mine_prob)

                    out, index_not_a_mine = self.model_adapter.predict(game.board, samples_index)
                    selected1_y = index_not_a_mine // dim2_w
                    selected2_x = index_not_a_mine % dim2_w

                    try:
                        game.open_cell(selected1_y, selected2_x)
                    except Exception:
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!')
                        print(f'{selected1_y},{selected2_x}')
                        print(f'{game.board.board_str()}')
                        print(f'index_not_a_mine: {index_not_a_mine}')
                        revealed_count = np.count_nonzero(game.board.board[:, :, 0] == 1)
                        mine_count = np.count_nonzero(game.board.board[:, :, 1] == 1)
                        out_count = np.count_nonzero(out.flatten() == 1)
                        print(f'revealed_count: {revealed_count}')
                        print(f'mine_count: {mine_count}')
                        print(f'out_count: {out_count}')
                        print(f'out: {np.reshape(out.flatten(), (16, 16))}')
                        # print(f'lay0:{np.reshape(get_layer(x_new, 0).flatten(), (16, 16))}')
                        # print(f'mine_prob: {mine_prob}')
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!')
                        raise

                    truth = self.truth_func(game.board, out, selected1_y, selected2_x)
                    self.model_adapter.y_data[samples_index] = truth

                    game_clicks += 1
                    samples_index += 1

                if game.game_over:
                    total_games_count += 1
                    games_count += 1
                    revealed_cells += game.opened_cells
                    clicks += game_clicks
                if game.game_won:
                    print('YEEEEEE, I WON!!!!!')
                    victories += 1
                    total_victories += 1

            fit_data = self.model_adapter.get_fit_data()
            history = self.model.fit(fit_data, self.model_adapter.y_data, batch_size=32,
                                     epochs=epochs, validation_split=0.3,
                                     callbacks=[tensorboard])
            loss = history.history['loss']
            mean_loss = sum(loss) / len(loss)
            val_loss = history.history['val_loss']
            val_loss = sum(val_loss) / len(val_loss)

            if games_count != 0:
                mean_clicks = float(clicks) / games_count
                mean_victories = float(victories) / games_count
                mean_revealed = float(revealed_cells) / games_count
            else:
                mean_clicks = float(clicks)
                mean_victories = 0.0
                mean_revealed = float(revealed_cells)

            print(f'Total games: {total_games_count}')
            print(f'Total victories: {total_victories}')

            print(f'Session games: {games_count}')
            print(f'Session mean clicks: {mean_clicks}')
            print(f'Session mean victories: {mean_victories}')
            print(f'Session mean cells revealed: {mean_revealed}')
            t = time.time() - started_at
            print(f'Session time: {t} seconds')

            self.log_file.write(
                f'{i},{mean_loss},{val_loss},{total_games_count},{total_victories},{games_count},'
                f'{mean_clicks},{mean_victories},{mean_revealed},{t}\n')
            self.log_file.flush()

            if (i + 1) % 10 == 0:
                self.model.save(f'models/{self.name}')

    @staticmethod
    def get_truth_from_predictions(board, model_predicted_out, y, x):
        truth = model_predicted_out[0]
        if len(truth.shape) == 3:
            truth[y, x, 0] = board.is_mine(y, x)
            return truth
        elif len(truth.shape) == 1:
            truth[y * board.board_width + x] = board.is_mine(y, x)
            return truth

    @staticmethod
    def get_truth_from_board(board, model_predicted_out, y, x):
        truth = model_predicted_out[0]
        for by in range(board.board_height):
            for bx in range(board.board_width):
                truth[by, bx, 0] = board.is_mine(by, bx)
        return truth

    @staticmethod
    def get_truth_from_neighbours(board, model_predicted_out, y, x):
        truth = model_predicted_out[0]
        for cy, cx in board.get_hidden_cells_near_revealed_cells():
            truth[cy, cx, 0] = board.is_mine(cy, cx)
        return truth

    def test(self, games_count):
        dim1_h, dim2_w = self.difficulty.dim1_height, self.difficulty.dim2_width
        revealed_cells = 0
        victories = 0
        for i in range(games_count):
            if (i % 10) == 0:
                print(f'Playing game {i + 1}...')
            game = Game(self.difficulty)
            game.open_cell(randint(0, dim1_h - 1), randint(0, dim2_w - 1))
            while not game.game_over:
                x = game.board.data
                x2 = flipped_revealed(x)
                out = self.model.predict([np.array([x]), np.array([x2])])
                ordered_probs = np.argsort(out[0][0] + x[0], axis=None)
                selected = ordered_probs[0]
                selected1_y = selected // dim2_w
                selected2_x = selected % dim2_w
                game.open_cell(selected2_x, selected1_y)
            revealed_cells += game.opened_cells
            if game.game_won:
                victories += 1
        victories = float(victories) / games_count
        mean_revealed = float(revealed_cells) / games_count
        print(f'Proportion of games won, batch {games_count}: {victories}')
        print(f'Mean cells revealed, batch " + {games_count}: {mean_revealed}')

    def play(self):
        dim1_h, dim2_w = self.difficulty.dim1_height, self.difficulty.dim2_width
        game = Game(self.difficulty)
        print('Beginning play')
        print('Game board:')
        print(game.board.board_str())
        selected1_y = randint(0, dim1_h - 1)
        selected2_x = randint(0, dim2_w - 1)
        game.open_cell(selected1_y, selected2_x)
        time.sleep(0.5)

        i = 0
        while not game.game_over:
            x = game.board.data
            x2 = flipped_revealed(x)
            out = self.model.predict([np.array([x]), np.array([x2])])

            print('out:')
            print(out)
            print('-----')
            print(x[0])

            ordered_probs = np.argsort(out[0][0] + x[0], axis=None)
            print('ordered probs')
            print(ordered_probs)

            selected = ordered_probs[0]
            selected1_y = selected // dim2_w
            selected2_x = selected % dim2_w
            print(f'select y: {selected1_y}')
            print(f'select x: {selected2_x}')

            game.open_cell(selected1_y, selected2_x)
            time.sleep(0.5)
            i += 1
            print(f'Selection {i}: ({selected1_y + 1}, {selected2_x + 1})')
            confidence = np.round(100 * (1 - np.amin(out[0][0] + x[0])), 2)
            print(f'Confidence: {confidence} %')
            print("Game board:")
            print(game.board.board_str())

        if game.game_won:
            print('Victory!')
        else:
            print('Game Over')
