import sys
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, LeakyReLU, BatchNormalization


class Model(object):

    def __init__(self, image_width, image_height, batch_size, characters):
        self.image_width = image_width
        self.image_height = image_height
        self.batch_size = batch_size
        self.characters = characters

        self.cnn_model = self.prepare_cnn()
        self.rnn_model = self.prepare_rnn()
        self.ctc = self.prepare_ctc()

    def prepare_cnn(self):
        cnn_model = Sequential()

        cnn_model.add(Conv2D(
            32,
            kernel_size=(5, 5),
            activation="relu",
            input_shape=(self.image_width, self.image_height, 1),
            padding="same"))
        cnn_model.add(BatchNormalization())
        cnn_model.add(LeakyReLU(alpha=0.1))
        cnn_model.add(MaxPooling2D((2, 2), padding="same"))

        cnn_model.add(Conv2D(
            64,
            kernel_size=(5, 5),
            activation="relu",
            input_shape=(self.image_width, self.image_height, 1),
            padding="same"))
        cnn_model.add(BatchNormalization())
        cnn_model.add(LeakyReLU(alpha=0.1))
        cnn_model.add(MaxPooling2D((2, 2), padding="same"))

        cnn_model.add(Conv2D(
            128,
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(self.image_width, self.image_height, 1),
            padding="same"))
        cnn_model.add(BatchNormalization())
        cnn_model.add(LeakyReLU(alpha=0.1))
        cnn_model.add(MaxPooling2D((2, 2), padding="same"))

        cnn_model.add(Conv2D(
            128,
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(self.image_width, self.image_height, 1),
            padding="same"))
        cnn_model.add(BatchNormalization())
        cnn_model.add(LeakyReLU(alpha=0.1))
        cnn_model.add(MaxPooling2D((2, 2), padding="same"))

        cnn_model.add(Conv2D(
            256,
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(self.image_width, self.image_height, 1),
            padding="same"))
        cnn_model.add(BatchNormalization())
        cnn_model.add(LeakyReLU(alpha=0.1))
        cnn_model.add(MaxPooling2D((1, 2), padding="same"))

        cnn_model.compile(
            loss=keras.losses.categorical_crossentropy,
            optimizer=keras.optimizers.Adam(),
            metrics=['accuracy'])
        cnn_model.summary()

        return cnn_model

    def prepare_rnn(self):
        pass

    def prepare_ctc(self):
        pass
