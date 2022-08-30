import numpy as np
import cv2

lut = np.asarray([
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 20
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 40
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 60
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 80
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 100
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 120
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 140
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 160
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 180
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 200
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 220
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 240
    0, 0, 0, 0, 0, 0, 0, 0, 30, 90, 120, 165, 200, 225, 245, 255])  # 256


def preprocess(image):
    # Crop
    img1 = image[260:260 + 84, 70:70 + 500]
    # Resize
    img2 = cv2.resize(img1, (180, 30), interpolation=cv2.INTER_NEAREST)
    # Isolate white pixels
    hsv = cv2.cvtColor(img2, cv2.COLOR_RGB2HSV)
    lower_white = np.array([0, 0, 0], dtype=np.uint8)
    upper_white = np.array([255, 30, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    img2 = cv2.bitwise_and(img2, img2, mask=mask)
    # Apply LUT
    img2 = cv2.LUT(img2, lut).astype('uint8')
    # Convert RGB to grayscale
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    # Dilate
    kernel = np.ones((3, 3), np.uint8)
    img2 = cv2.dilate(img2, kernel, iterations=1)
    # Resize
    img3 = cv2.resize(img2, (60, 10), interpolation=cv2.INTER_NEAREST)
    # Rescale 0-255 to 0-1
    img3 = img3 / 255
    # Expand dimensions from (10, 60) to (10, 60, 1)
    img3 = np.expand_dims(img3, axis=2)
    # Rearrange array dimensions (10, 60, 1) to (1, 10, 60)
    img3 = img3.transpose((2, 0, 1))
    return img3
