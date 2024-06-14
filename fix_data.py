import numpy as np
from PIL import Image
import os


def resize_image(input_path, output_path, size):
        """
        Resize an image to the specified size and save it to a new file.

        :param input_path: Path to the input image file.
        :param output_path: Path to save the resized image file.
        :param size: Tuple (width, height) to resize the image to.
        """
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize(size)
            
            # Save the resized image
            resized_img.save(output_path)

path = "./train_0.png"

image = Image.open(path)
image_array = np.array(image)
print(np.shape(image_array))
print(image_array[3])
print(image_array[0])

# resize_image(path, path, (600, 315, 3))

# image = Image.open(path)
# image_array = np.array(image)
# print(np.shape(image_array))