import cv2


def preprocess(image):
    # Crop
    image = image[160:, :]
    # Resize
    image = cv2.resize(image, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
    # Rescale 0-255 to 0-1
    image = image / 255
    # Rearrange array dimensions (32, 64, 3) to (3, 32, 64)
    image = image.transpose((2, 0, 1))

    return image
