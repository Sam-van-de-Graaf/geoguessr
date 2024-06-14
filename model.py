import numpy as np
from PIL import Image
import keras
import time

from keras.models import Sequential
from keras.layers import CategoryEncoding, Dense, Activation, Conv2D, Input, Flatten, MaxPooling2D, Dropout
from keras.optimizers import SGD
from keras import utils
from keras.models import load_model

from data_pre import data_pre

x_train = np.load("sams_set_X_train.npy")
y_train = np.load("sams_set_Y_train.npy")

# x_train, y_train = data_pre(x_train, y_train)

# print(image_array)
# print(image_array.shape)  # Print the shape of the array
# print(type(image_array))

# model = Sequential()
# model.add(Input(shape=(420, 2568, 3)))

# model.add(Conv2D(16, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(16, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Conv2D(32, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(32, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Conv2D(64, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(64, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Conv2D(128, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(128, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Conv2D(256, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(256, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Conv2D(512, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Conv2D(512, kernel_size=3, activation='relu', padding='same'))
# model.add(Conv2D(512, kernel_size=3, activation='relu', padding='same'))
# model.add(MaxPooling2D(2, 2))
# model.add(Flatten())
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(2, activation='tanh'))

# # model.summary()

# model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

for i in range(30):
    model = load_model("sams_model.keras")

    start_time = time.time()
    model.fit(x_train, y_train, epochs=1, verbose=1)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")

    model.save("sams_model.keras")