from keras.models import Model
from keras.layers import Input
from keras.layers import Conv2D
from keras.layers import Multiply

from difficulty import Difficulty


def conv2d_relu_sigmoid_binarycrosse_adam1(difficulty: Difficulty):
    input_shape = (difficulty.dim1_height, difficulty.dim2_width, 11)  # 11 channels

    in1 = Input(shape=input_shape)
    conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(in1)
    conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
    conv = Conv2D(1, (1, 1), padding='same', activation='sigmoid', use_bias=True)(conv)

    in2 = Input(shape=(difficulty.dim1_height, difficulty.dim2_width, 1))
    out = Multiply()([conv, in2])

    model = Model(inputs=[in1, in2], outputs=out)
    model.compile(loss='binary_crossentropy', optimizer='adam')

    return model
