import time
from random import randint

import numpy as np
from tensorflow.keras.callbacks import TensorBoard

from game import Game


def flipped_revealed(np_board):
    dim1, dim2 = np_board.shape[0:2]
    return np.ones((dim1, dim2, 1)) - np_board[:, :, 0:1]
    # result = np.zeros((dim1, dim2, 1))
    # for x in range(dim1):
    #    for y in range(dim2):
    #        result[x][y][0] = 1 - np_board[x][y][0]
    # return result


def get_layer(np_board, lay):
    return np_board[:, :, lay]


class Brain:
    def __init__(self, model, difficulty, name, log_file, truth_source='predictions'):
        self.model = model
        self.difficulty = difficulty
        self.name = name
        self.truth_func = getattr(self, 'get_truth_from_' + truth_source, self.get_truth_from_predictions)
        self.log_file = log_file

    def learn(self, samples, sessions, epochs):
        dim1_h, dim2_w = self.dimensions()
        x_data = np.zeros((samples, dim1_h, dim2_w, 11))
        x2_data = np.zeros((samples, dim1_h, dim2_w, 1))
        y_data = np.zeros((samples, dim1_h, dim2_w, 1))

        tensorboard = TensorBoard(log_dir=f"tensor_logs/{self.name}")

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
                game.open_cell(randint(0, dim2_w - 1), randint(0, dim1_h - 1))
                game_clicks = 0
                while not game.game_over and samples_index != samples:
                    x_new = self.get_channels(game.board)
                    x_data[samples_index] = x_new
                    # flip
                    x2_new = flipped_revealed(x_new)
                    x2_data[samples_index] = x2_new

                    out = self.model.predict([np.array([x_new]), np.array([x2_new])])

                    mine_prob = out.flatten() + get_layer(x_new, 0).flatten()
                    index_not_a_mine = np.argmin(mine_prob)
                    selected1_y = index_not_a_mine // dim2_w
                    selected2_x = index_not_a_mine % dim2_w
                    game.open_cell(selected2_x, selected1_y)

                    truth = self.truth_func(game.board, out, selected2_x, selected1_y)
                    y_data[samples_index] = truth

                    game_clicks += 1
                    samples_index += 1

                if game.game_over:
                    total_games_count += 1
                    games_count += 1
                    revealed_cells += game.opened_cells
                    clicks += game_clicks
                if game.game_won:
                    print("YEEEEEE, I WON!!!!!")
                    victories += 1
                    total_victories += 1

            history = self.model.fit([x_data, x2_data], y_data, batch_size=32,
                                     epochs=epochs, validation_split=0.3,
                                     callbacks=[tensorboard])
            loss = history.history['loss']
            mean_loss = sum(loss) / len(loss)
            val_loss = history.history['val_loss']
            val_loss = sum(val_loss) / len(val_loss)

            mean_clicks = float(clicks) / games_count
            mean_victories = float(victories) / games_count
            mean_revealed = float(revealed_cells) / games_count
            print(f"Total games: {total_games_count}")
            print(f"Total victories: {total_victories}")

            print(f"Session games: {games_count}")
            print(f"Session mean clicks: {mean_clicks}")
            print(f"Session mean victories: {mean_victories}")
            print(f"Session mean cells revealed: {mean_revealed}")
            t = time.time() - started_at
            print(f"Session time: {t} seconds")

            self.log_file.write(
                f'{i},{mean_loss},{val_loss},{total_games_count},{total_victories},{games_count},{mean_clicks},{mean_victories},{mean_revealed},{t}\n')
            self.log_file.flush()

            if (i + 1) % 10 == 0:
                self.model.save("models/" + self.difficulty.name + '_' + self.name)

    @staticmethod
    def get_truth_from_predictions(board, model_predicted_out, x, y):
        truth = model_predicted_out[0]
        truth[y, x, 0] = int(board.get_cell(x, y).mine)
        return truth

    @staticmethod
    def get_truth_from_board(board, model_predicted_out, x, y):
        truth = model_predicted_out[0]
        for by in range(board.board_height):
            for bx in range(board.board_width):
                cell = board.get_cell(bx, by)
                if cell.mine:
                    truth[by, bx, 0] = 1
        return truth

    @staticmethod
    def get_truth_from_neighbours(board, model_predicted_out, x, y):
        truth = model_predicted_out
        for cell in board.get_hidden_cells_near_revealed_cells():
            if cell.mine:
                truth[cell.y, cell.x, 0] = 1
        return truth

    def get_channels(self, board):
        dim1, dim2 = self.dimensions()
        out = np.zeros((dim1, dim2, 11))

        for y in range(dim1):
            for x in range(dim2):
                out[y][x][1] = 1  # border detection?
                cell = board.get_cell(x, y)
                if cell.revealed:
                    out[y][x][0] = 1  # revealed
                    out[y][x][cell.value + 2] = 1
        return out

    def dimensions(self):
        return self.difficulty.dim1_height, self.difficulty.dim2_width

    def test(self, games_count):
        dim = self.dimensions()
        dim1_h = dim[0]
        dim2_w = dim[1]
        revealed_cells = 0
        victories = 0
        for i in range(games_count):
            if (i % 10) == 0:
                print("Playing game " + str(i + 1) + "...")
            game = Game(self.difficulty)
            game.open_cell(randint(0, dim2_w - 1), randint(0, dim1_h - 1))
            while not game.game_over:
                x = self.get_channels(game.board)
                x2 = np.array([np.where(x[0] == 0, 1, 0)])
                x_swapped = np.swapaxes(x, 0, 2)
                x2_swapped = np.swapaxes(x2, 0, 2)
                out = self.model.predict([np.array([x_swapped]), np.array([x2_swapped])])
                ordered_probs = np.argsort(out[0][0] + x[0], axis=None)
                selected = ordered_probs[0]
                selected1_y = int(selected / dim2_w)
                selected2_x = selected % dim2_w
                game.open_cell(selected2_x, selected1_y)
            revealed_cells += game.opened_cells
            if game.game_won:
                victories += 1
        victories = float(victories) / games_count
        mean_revealed = float(revealed_cells) / games_count
        print("Proportion of games won, batch " + str(games_count) + ": " + str(victories))
        print("Mean cells revealed, batch " + str(games_count) + ": " + str(mean_revealed))

    def play(self):
        game = Game(self.difficulty)
        print("Beginning play")
        print("Game board:")
        print(game.board)
        selected1 = randint(0, game.board.board_height - 1)
        selected2 = randint(0, game.board.board_width - 1)
        game.open_cell(selected1, selected2)
        time.sleep(0.5)

        i = 0
        while not game.game_over:
            print("Last selection " + str(i) + ": (" + str(selected1 + 1) + "," + str(selected2 + 1) + ")")
            if 'out' in locals():
                print("Confidence: " + str(np.round(100 * (1 - np.amin(out[0][0] + x_new[0])), 2)) + "%")
            print("Game board:")
            print(game.board)

            x_new = self.get_channels(game.board)
            x2_new = np.array([np.where(x_new[0] == 0, 1, 0)])
            x_swapped = np.swapaxes(x_new, 0, 2)
            x2_swapped = np.swapaxes(x2_new, 0, 2)
            out = self.model.predict([np.array([x_swapped]), np.array([x2_swapped])])

            print('out:')
            print(out)
            print('-----')
            print(x_new[0])

            ordered_probs = np.argsort(out[0][0] + x_new[0], axis=None)
            print('ordered probs')
            print(ordered_probs)

            selected = ordered_probs[0]
            selected1 = int(selected / game.board.board_width)
            selected2 = selected % game.board.board_width
            print('select 1: ' + str(selected1) + '\nselect2: ' + str(selected2))

            game.open_cell(selected1, selected2)
            time.sleep(0.5)
            i += 1

        print("Last selection " + str(i) + ": (" + str(selected1 + 1) + "," + str(selected2 + 1) + ")")
        print("Confidence: " + str(np.round(100 * (1 - np.amin(out[0][0] + x_new[0])), 2)) + "%")
        print("Game board:")
        print(game.board)
        if game.game_won:
            print("Victory!")
        else:
            print("Game Over")
