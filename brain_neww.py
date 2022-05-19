import time
from random import randint

import numpy as np

from game import Game


def flipped_revealed(np_board):
    dim1, dim2 = np_board.shape[0:2]
    result = np.zeros((dim1, dim2, 1))
    for x in range(dim1):
        for y in range(dim2):
            result[x][y][0] = 1 - np_board[x][y][0]
    return result


def get_layer(np_board, lay):
    return np_board[:, :, lay]


class Brain:
    def __init__(self, model, difficulty, name):
        self.model = model
        self.difficulty = difficulty
        self.name = name

    def learn(self, sessions: int, samples: int, epochs: int):
        dim1, dim2 = self.dimensions()
        x_data = np.zeros((samples, dim1, dim2, 11))
        x2_data = np.zeros((samples, dim1, dim2, 1))
        y_data = np.zeros((samples, dim1, dim2, 1))

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
                randint1 = randint(0, dim1 - 1)
                randint2 = randint(0, dim2 - 1)
                #print(randint1, randint2)
                game.open_cell(randint1, randint2)

                while not game.game_over and samples_index != samples:
                    x = self.get_channels(game.board)
                    x_data[samples_index] = x
                    x2 = flipped_revealed(x)
                    x2_data[samples_index] = x2

                    out = self.model.predict([np.array([x]), np.array([x2])])
                    flat = out.flatten()
                    lay = get_layer(x, 0)
                    flat_lay = lay.flatten()
                    mine_prob = flat + flat_lay
                    selected = np.argmin(mine_prob)

                    if dim1 == dim2:
                        selected1 = selected // dim1
                        selected2 = selected % dim1
                    else:
                        selected1 = selected % dim1
                        selected2 = selected // dim1

                    print(selected, selected1, selected2, dim1, dim2)

                    game.open_cell(selected1, selected2)
                    clicks += 1

                    truth = out[0]

                    # print('place learn', selected1, 'of', dim1)
                    # print('place learn', selected2, 'of', dim2)
                    # print()

                    truth[selected1, selected2, 0] = int(
                        game.board.get_cell(selected1, selected2).mine)  # mines[selected1, selected2]
                    y_data[samples_index] = truth

                    samples_index += 1


                total_games_count += 1
                games_count += 1
                revealed_cells += game.opened_cells
                if game.game_won:
                    print('YEEEEEE, I WON!!!!!')
                    victories += 1
                    total_victories += 1

            self.model.fit([x_data, x2_data], y_data, batch_size=32, epochs=epochs)

            mean_clicks = float(clicks) / games_count
            mean_victories = float(victories) / games_count
            mean_revealed = float(revealed_cells) / games_count
            print(f'Total games: {total_games_count}')
            print(f'Total victories: {total_victories}')

            print(f'Session games: {games_count}')
            print(f'Session mean clicks: {mean_clicks}')
            print(f'Session mean victories: {mean_victories}')
            print(f'Session mean cells revealed: {mean_revealed}')
            print(f'Session time: {time.time() - started_at} seconds')

            if (i + 1) % 10 == 0:
                self.model.save('models/' + self.difficulty + '_' + self.name)

    def get_channels(self, board):
        dim1, dim2 = self.dimensions()
        out = np.zeros((dim1, dim2, 11))

        for x in range(dim1):
            for y in range(dim2):
                out[x][y][1] = 1
                # print('channels', x, 'of', dim1)
                # print('channels', y, 'of', dim2)
                # print()

                cell = board.get_cell(x, y)
                if cell.revealed:
                    out[x][y][0] = 1
                    out[x][y][cell.value + 2] = 1
        return out

    def dimensions(self):
        if self.difficulty == 'beginner':
            return 8, 8
        elif self.difficulty == 'intermediate':
            return 16, 16
        elif self.difficulty == 'expert':
            return 16, 30
        else:
            raise Exception

    def test(self, games_count):
        dim1, dim2 = self.dimensions()
        total_victories = 0
        revealed_cells = 0
        clicks = 0
        for i in range(games_count):
            if i % 10 == 0:
                print(f'Playing {i}...')
            game = Game(self.difficulty)
            game.open_cell(randint(0, dim1 - 1), randint(0, dim2 - 1))

            while not game.game_over:
                x = self.get_channels(game.board)
                x2 = flipped_revealed(x)

                out = self.model.predict([np.array([x]), np.array([x2])])
                mine_prob = out.flatten() + get_layer(x, 0).flatten()
                selected = np.argmin(mine_prob)
                selected1 = selected // dim2
                selected2 = selected % dim2

                game.open_cell(selected1, selected2)
                clicks += 1
            revealed_cells += game.opened_cells
            if game.game_won:
                total_victories += 1

        mean_clicks = float(clicks) / games_count
        mean_victories = float(total_victories) / games_count
        mean_revealed = float(revealed_cells) / games_count
        print(f'Total games: {games_count}')
        print(f'Total victories: {total_victories}')

        print(f'Session games: {games_count}')
        print(f'Session mean clicks: {mean_clicks}')
        print(f'Session mean victories: {mean_victories}')
        print(f'Session mean cells revealed: {mean_revealed}')

    def play(self):
        dim1, dim2 = self.dimensions()
        game = Game(self.difficulty)

        print('Beginning play')
        print('Game board:')
        print(game.board)

        selected1 = randint(0, dim1 - 1)
        selected2 = randint(0, dim2 - 1)
        game.open_cell(selected1, selected2)
        time.sleep(0.5)

        i = 0
        while not game.game_over:
            print(f'Open cell: {i}:({selected1 + 1}, {selected2 + 1})')
            if 'out' in locals():
                print(f'Confidence: {np.round(100 * (1 - np.amin(out[0][0] + x[0])), 2)}%')
            print('Game board:')
            print(game.board)

            x = self.get_channels(game.board)
            x2 = flipped_revealed(x)

            out = self.model.predict([np.array([x]), np.array([x2])])
            mine_prob = out.flatten() + get_layer(x, 0).flatten()
            selected = np.argmin(mine_prob)
            selected1 = selected // dim2
            selected2 = selected % dim2

            game.open_cell(selected1, selected2)
            time.sleep(0.5)

            i += 1

        print(f'Open cell: {i}:({selected1 + 1}, {selected2 + 1})')
        print(f'Confidence: {np.round(100 * (1 - np.amin(out[0][0] + x[0])), 2)}%')

        print('Game board:')
        print(game.board)
        if game.game_won:
            print('Tonight we are victorious!')
        else:
            print('Game Over! For now...')
