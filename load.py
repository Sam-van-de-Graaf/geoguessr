import numpy as np
from PIL import Image
import os
from data_pre import data_pre

def load_training():

    keep_loading = True
    i = 0

    image_array = []
    while keep_loading:
        if os.path.isfile("./training_data/x_data/train_" + str(i) + ".png"):
            image = Image.open("./training_data/x_data/train_" + str(i) + ".png")
            image = np.array(image)
            image_array.append(image)
        else:
            keep_loading = False
        i += 1
    image_array = np.array(image_array)

    y_data = []
    with open("./training_data/y_data/y_data.txt", 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            for x in lines:
                if len(x) >= 2:
                    dictionary = eval(x)
                    y_data.append((dictionary["lat"], dictionary["lng"]))
    y_data = np.array(y_data)

    image_array, y_data = data_pre(image_array, y_data)
    np.save("sams_set_Y_train.npy", y_data)
    np.save("sams_set_X_train.npy", image_array)

def load_testing():
     
    keep_loading = True
    i = 0

    image_array = []
    while keep_loading:
        if os.path.isfile("./testing_data/x_data/test_" + str(i) + ".png"):
            image = Image.open("./testing_data/x_data/test_" + str(i) + ".png")
            image = np.array(image)
            image_array.append(image)
        else:
            keep_loading = False
        i += 1
    image_array = np.array(image_array)

    y_data = []
    with open("./testing_data/y_data/y_data.txt", 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            for x in lines:
                if len(x) >= 2:
                    dictionary = eval(x)
                    y_data.append((dictionary["lat"], dictionary["lng"]))
    y_data = np.array(y_data)
    
    image_array, y_data = data_pre(image_array, y_data)
    np.save("sams_set_Y_test.npy", y_data)
    np.save("sams_set_X_test.npy", image_array)


load_testing()
load_training()

images = np.load("sams_set_X_test.npy")
print(np.shape(images))
print(len(images))
# print(images[2279])

test = np.load("sams_set_Y_test.npy")
print(np.shape(test))
# print(len(test))
