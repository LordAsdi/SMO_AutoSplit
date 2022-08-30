import numpy as np
import cv2

frame_hist = []


def preprocess(image):
    # Resize
    image = cv2.resize(image, (32, 24), interpolation=cv2.INTER_NEAREST)
    # Convert RGB to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Threshold at 1
    th, image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
    # Rescale 0-255 to 0-1
    image = image / 255
    # Expand dimensions from (24, 32) to (24, 32, 1)
    image = np.expand_dims(image, axis=2)
    # Rearrange array dimensions (24, 32, 1) to (1, 24, 32)
    image = image.transpose((2, 0, 1))

    # Create image array
    frame_hist.append(image)
    if len(frame_hist) > 19:
        frame_hist.pop(0)

    if len(frame_hist) < 19:
        return np.zeros((1, 24, 320))

    image_array = frame_hist[0]

    # Create array of every second frame
    for image in frame_hist[1::2]:
        image_array = np.concatenate((image_array, image), axis=2)

    return image_array
