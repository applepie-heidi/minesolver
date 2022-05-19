from keras.layers import Input
from keras.layers.convolutional import Conv2D
from keras.layers.merge import Multiply
from keras.models import Model

dim1 = 16
dim2 = 30
input_shape = (dim1, dim2, 11)  # 11 channels

in1 = Input(shape=input_shape)
conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(in1)
conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
conv = Conv2D(64, (3, 3), padding='same', activation='relu', use_bias=True)(conv)
conv = Conv2D(1, (1, 1), padding='same', activation='sigmoid', use_bias=True)(conv)

in2 = Input(shape=(dim1, dim2, 1))
out = Multiply()([conv, in2])

model = Model(inputs=[in1, in2], outputs=out)
model.compile(loss='binary_crossentropy', optimizer='adam')
