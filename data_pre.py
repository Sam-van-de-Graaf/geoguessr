import numpy as np

def data_pre(x_data, y_data):
    x_data = x_data[:] / 255
    y_data = np.array([(x[0] / 90, x[1] / 180) for x in y_data])
    return (x_data, y_data)

def data_post(x_data, y_data):
    x_data = x_data[:] * 255
    y_data = np.array([(x[0] * 90, x[1] * 180) for x in y_data])
    return (x_data, y_data)