from keras.models import Model
import keras.layers as kl

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

    return model


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

    return model


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

    return model


def dense_relu_softmax_binarycrosse_adam1(difficulty: Difficulty):
    input_shape = (difficulty.dim1_height, difficulty.dim2_width, 11)  # 11 channels

    in1 = kl.Input(shape=input_shape)
    dense = kl.Dense(3000, activation='relu')(in1)
    dense = kl.Dense(1000, activation='relu')(dense)
    dense = kl.Dense(10, activation='relu')(dense)
    dense = kl.Dense(1, activation='softmax', use_bias=True)(dense)

    in2 = kl.Input(shape=(difficulty.dim1_height, difficulty.dim2_width, 1))
    out = kl.Multiply()([dense, in2])

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model
