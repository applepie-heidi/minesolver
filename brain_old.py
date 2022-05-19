import time
from random import randint

import numpy as np

from game import Game


class Brain:
    def __init__(self, model, difficulty, name):
        self.model = model
        self.difficulty = difficulty
        self.name = name

    def learn(self, samples, batches, epochs):
        dim = self.dimensions()
        dim1 = dim[0]
        dim2 = dim[1]
        x_data = np.zeros((samples, 11, dim1, dim2))
        x2_data = np.zeros((samples, 1, dim1, dim2))
        y_data = np.zeros((samples, 1, dim1, dim2))

        for i in range(batches):
            samples_count = 0
            while samples_count < samples:
                game = Game(self.difficulty)
                while game.open_cell(randint(0, dim1), randint(0, dim2)):
                    pass
                while not game.game_over and samples_count != samples:
                    x_new = self.get_channels(game.board)
                    x_data[samples_count] = x_new
                    x2_new = np.array([np.where(x_new[0] == 0, 1, 0)])
                    x2_data[samples_count] = x2_new

                    out = self.model.predict([np.array([x_new]), np.array([x2_new])])

                    ordered_probs = np.argsort(out[0][0] + x_new[0], axis=None)
                    selected = ordered_probs[0]
                    selected1 = int(selected / dim2)
                    selected2 = selected % dim2
                    game.open_cell(selected1, selected2)
                    # find truth
                    mines = np.zeros((dim1, dim2))
                    for x in range(dim1):
                        for y in range(dim2):
                            if game.board.get_cell(x, y).mine:
                                mines[x][y] = 1

                    truth = out
                    # print(out)
                    truth[0, 0, selected1, selected2] = mines[selected1, selected2]
                    y_data[samples_count] = truth[0, 0]

                    samples_count += 1

            self.model.fit([x_data, x2_data], y_data, batch_size=samples, epochs=epochs)
            if (i + 1) % 10 == 0:
                self.model.save("models/" + self.difficulty + '_' + self.name)

    def get_channels(self, board):
        dim = self.dimensions()
        dim1 = dim[0]
        dim2 = dim[1]
        out = np.zeros((11, dim1, dim2))

        # is on game board
        out[1] = np.ones((dim1, dim2))

        for x in range(dim1):
            for y in range(dim2):
                # is revealed
                cell = board.get_cell(x, y)
                if cell.revealed:
                    out[0][x][y] = 1

                    # neighbours
                    for i in range(0, 9):
                        if cell.value == i:
                            out[i + 2][x][y] = 1

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
        dim = self.dimensions()
        dim1 = dim[0]
        dim2 = dim[1]
        revealed_cells = 0
        victories = 0
        for i in range(games_count):
            if (i % 10) == 0:
                print("Playing game " + str(i + 1) + "...")
            game = Game(self.difficulty)
            game.open_cell(randint(0, dim1), randint(0, dim2))
            while not game.game_over:
                x = self.get_channels(game.board)
                x2 = np.array([np.where(x[0] == 0, 1, 0)])
                out = self.model.predict([np.array([x]), np.array([x2])])
                ordered_probs = np.argsort(out[0][0] + x[0], axis=None)
                selected = ordered_probs[0]
                selected1 = int(selected / dim2)
                selected2 = selected % dim2
                game.open_cell(selected1, selected2)
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
        selected1 = randint(0, game.board.board_height)
        selected2 = randint(0, game.board.board_width)
        game.open_cell(selected1, selected2)
        time.sleep(0.5)
        i = 0
        while not game.game_over:
            print("Last selection " + str(i) + ": (" + str(selected1 + 1) + "," + str(selected2 + 1) + ")")
            if 'out' in locals():
                print("Confidence: " + str(np.round(100 * (1 - np.amin(out[0][0] + Xnow[0])), 2)) + "%")
            print("Game board:")
            print(game.board)
            Xnow = self.get_channels(game.board)
            X2now = np.array([np.where(Xnow[0] == 0, 1, 0)])
            out = self.model.predict([np.array([Xnow]), np.array([X2now])])
            print('out:')
            print(out)
            print('-----')
            print(Xnow[0])
            orderedProbs = np.argsort(out[0][0] + Xnow[0], axis=None)
            print('ordered probs')
            print(orderedProbs)
            selected = orderedProbs[0]
            selected1 = int(selected / game.board.board_width)
            selected2 = selected % game.board.board_width
            print('select 1: ' + str(selected1) + '\nselect2: ' + str(selected2))
            game.open_cell(selected1, selected2)
            time.sleep(0.5)
            i += 1
        print("Last selection " + str(i) + ": (" + str(selected1 + 1) + "," + str(selected2 + 1) + ")")
        print("Confidence: " + str(np.round(100 * (1 - np.amin(out[0][0] + Xnow[0])), 2)) + "%")
        print("Game board:")
        print(game.board)
        if game.game_won:
            print("Victory!")
        else:
            print("Game Over")
