import numpy as np


class CompassDetector:
    def __init__(self):
        self.red_pixels = 0
        self.prev_red_pixel_count = 0

    def update(self, frame):
        # This method does not work well with compressed video
        if self.red_pixels > 0:
            self.prev_red_pixel_count += 1
        else:
            self.prev_red_pixel_count = 0

        frame_crop = frame[123:123 + 25, 586:586 + 23]
        self.red_pixels = np.sum([[y[0] > 210 and y[1] < 20 and y[2] < 20 for y in x] for x in frame_crop])

    def check_compass(self):
        if self.red_pixels == 0 and self.prev_red_pixel_count > 10:
            return True

        return False
