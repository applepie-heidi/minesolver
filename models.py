import numpy as np
from keras.models import Model
import keras.layers as kl

from board import Board
from difficulty import Difficulty


def conv2d_relu_sigmoid_binarycrosse_adam1(difficulty: Difficulty):
    input_shape = (difficulty.dim1_height, difficulty.dim2_width, 11)  # 11 channels

    in1 = kl.Input(shape=input_shape)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(in1)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = kl.Conv2D(1, (1, 1), padding='same', activation='sigmoid', use_bias=True)(conv)

    in2 = kl.Input(shape=(difficulty.dim1_height, difficulty.dim2_width, 1))
    out = kl.Multiply()([conv, in2])

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, ModelConv2DAdapter()


def conv2d_relu_softmax_binarycrosse_adam1(difficulty: Difficulty):
    input_shape = (difficulty.dim1_height, difficulty.dim2_width, 11)  # 11 channels

    in1 = kl.Input(shape=input_shape)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(in1)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = kl.Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = kl.Conv2D(1, (1, 1), padding='same', activation='softmax', use_bias=True)(conv)

    in2 = kl.Input(shape=(difficulty.dim1_height, difficulty.dim2_width, 1))
    out = kl.Multiply()([conv, in2])

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, ModelConv2DAdapter()


def conv2d_maxpooling_dense_relu_softmax_binarycrosse_adam1(difficulty: Difficulty):
    input_shape = (difficulty.dim1_height, difficulty.dim2_width, 11)  # 11 channels

    in1 = kl.Input(shape=input_shape)
    conv = kl.Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(in1)
    conv = kl.MaxPooling2D((2, 2))(conv)
    conv = kl.Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu')(conv)
    conv = kl.MaxPooling2D((2, 2))(conv)
    flat = kl.Flatten()(conv)
    dense = kl.Dense(64, activation='relu')(flat)
    dense = kl.Dense(1, activation='softmax', use_bias=True)(dense)

    in2 = kl.Input(shape=(difficulty.dim1_height, difficulty.dim2_width, 1))
    out = kl.Multiply()([dense, in2])

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, ModelConv2DAdapter()


def dense_relu_sigmoid_binarycrosse_adam1(difficulty: Difficulty):
    n = difficulty.dim1_height * difficulty.dim2_width

    in1 = kl.Input(shape=(n,))
    dense = kl.Dense(n * 16, activation='relu')(in1)
    dense = kl.Dense(n * 8, activation='relu')(dense)
    dense = kl.Dense(n, activation='sigmoid')(dense)

    in2 = kl.Input(shape=(n,))
    out = kl.Multiply()([dense, in2])

    print(dense.get_shape())
    print(out.get_shape())

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, ModelDenseAdapter()


def dense_relu_sigmoid_binarycrosse_adam2(difficulty: Difficulty):
    n = difficulty.dim1_height * difficulty.dim2_width

    in1 = kl.Input(shape=(n,))
    dense = kl.Dense(n * 50, activation='relu')(in1)
    dense = kl.Dense(n * 25, activation='relu')(dense)
    dense = kl.Dense(n, activation='sigmoid')(dense)

    in2 = kl.Input(shape=(n,))
    out = kl.Multiply()([dense, in2])

    print(dense.get_shape())
    print(out.get_shape())

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, ModelDenseAdapter()


def dense_relu_sigmoid_binarycrosse_adam3(difficulty: Difficulty):
    n = difficulty.dim1_height * difficulty.dim2_width

    in1 = kl.Input(shape=(n,))
    dense = kl.Dense(n * 50, activation='relu')(in1)
    dense = kl.Dense(n * 25, activation='relu')(dense)
    dense = kl.Dense(n * 15, activation='relu')(dense)
    dense = kl.Dense(n, activation='sigmoid')(dense)

    in2 = kl.Input(shape=(n,))
    out = kl.Multiply()([dense, in2])

    print(dense.get_shape())
    print(out.get_shape())

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model, ModelDenseAdapter()


def flipped_revealed(np_board):
    dim1, dim2 = np_board.shape[0:2]
    return np.ones((dim1, dim2, 1)) - np_board[:, :, 0:1]


def get_layer(np_board, lay):
    return np_board[:, :, lay]


class ModelAdapter:
    def __init__(self):
        self.model = None
        self.y_data = None  # type: np.array

    def adapt(self, model, difficulty: Difficulty, samples: int):
        pass

    def predict(self, board: Board, sample_index: int):
        pass

    def get_fit_data(self):
        pass


class ModelConv2DAdapter(ModelAdapter):
    def __init__(self):
        super().__init__()
        self.x_data = None
        self.x2_data = None

    def adapt(self, model, difficulty: Difficulty, samples: int):
        self.model = model
        self.x_data = np.zeros((samples, difficulty.dim1_height, difficulty.dim2_width, 11))
        self.x2_data = np.zeros((samples, difficulty.dim1_height, difficulty.dim2_width, 1))
        self.y_data = np.zeros((samples, difficulty.dim1_height, difficulty.dim2_width, 1))

    def predict(self, board: Board, sample_index: int):
        x_new = board.data
        self.x_data[sample_index] = x_new

        x2_new = flipped_revealed(x_new)  # 1 -> hidden, 0 -> revealed
        self.x2_data[sample_index] = x2_new

        inp = [np.array([x_new]), np.array([x2_new])]
        out = self.model.predict(inp)

        mine_prob = out.flatten() + get_layer(board.board, 0).flatten()
        return out, int(np.argmin(mine_prob))

    def get_fit_data(self):
        return [self.x_data, self.x2_data]


class ModelDenseAdapter(ModelAdapter):
    def __init__(self):
        super().__init__()
        self.x_data = None
        self.x2_data = None

    def adapt(self, model, difficulty: Difficulty, samples: int):
        self.model = model
        n = difficulty.dim1_height * difficulty.dim2_width
        self.x_data = np.zeros((samples, n))  # TODO is `1`` needed?
        self.x2_data = np.zeros((samples, n))  # TODO is `1`` needed?
        self.y_data = np.zeros((samples, n))

    def predict(self, board: Board, sample_index: int):
        revealed_layer = get_layer(board.board, 0)
        hint_layer = get_layer(board.board, 2)

        x_new = hint_layer.copy()
<<<<<<< HEAD
        x_new[revealed_layer == 0] = -8
        x_new = x_new.flatten()
        x_new = (x_new + 8) / 16.0
=======
        x_new[revealed_layer == 0] = -1
        x_new = x_new.flatten()  # TODO need? shape == (n,)
>>>>>>> parent of f28c2d0... fixed board
        self.x_data[sample_index] = x_new  # Save for later fit()

        x2_new = flipped_revealed(board.data).flatten()  # 1 -> hidden, 0 -> revealed
        self.x2_data[sample_index] = x2_new

        inp = [np.array([x_new]), np.array([x2_new])]
        out = self.model.predict(inp)

        mine_prob = out[0] + revealed_layer.flatten()
        return out, int(np.argmin(mine_prob))

    def get_fit_data(self):
        return [self.x_data, self.x2_data]


if __name__ == '__main__':
    from difficulty import BEGINNER, EXPERT

    dense_relu_sigmoid_binarycrosse_adam1(BEGINNER)
