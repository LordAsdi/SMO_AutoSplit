import numpy as np
import cv2


def preprocess(image):
    # Crop
    image = image[219:219 + 126, 15:15 + 19]
    # Threshold at 50
    th, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
    # Convert RGB to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Threshold at 200
    th, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
    # Resize
    image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
    # Rescale 0-255 to 0-1
    image = image / 255
    # Expand dimensions from (63, 10) to (63, 10, 1)
    image = np.expand_dims(image, axis=2)
    # Rearrange array dimensions (63, 10, 1) to (1, 63, 10)
    image = image.transpose((2, 0, 1))

    return image
