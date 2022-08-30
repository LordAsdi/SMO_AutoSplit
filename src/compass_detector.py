import numpy as np


class CompassDetector:
    def __init__(self):
        self.red_pixels = 0
        self.prev_red_pixel_count = 0

    def update(self, frame):
        if self.red_pixels > 0:
            self.prev_red_pixel_count += 1
        else:
            self.prev_red_pixel_count = 0

        frame_crop = frame[123:123 + 25, 586:586 + 23]
        self.red_pixels = np.sum([[y[0] > 220 and y[1] < 10 and y[2] < 10 for y in x] for x in frame_crop])

    def check_compass(self):
        print(self.red_pixels)
        print(self.prev_red_pixel_count)

        if self.red_pixels == 0 and self.prev_red_pixel_count > 10:
            return True

        return False
