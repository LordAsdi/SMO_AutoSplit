import numpy as np
import time
import cv2

import src.classifiers.odyssey.preprocessing as odyssey_prep
import src.classifiers.cap_end.preprocessing as cap_end_prep
import src.classifiers.moon_end.preprocessing as moon_end_prep
from src.classifiers.classifier import Classifier


class KingdomEndDetector:
    def __init__(self):
        # Classifiers
        self.odyssey_classifier = None
        self.cap_end_classifier = None
        self.moon_end_classifier = None

        # Model Paths
        self.odyssey_model_path = 'models/odyssey.onnx'
        self.cap_end_model_path = 'models/cap_end.onnx'
        self.moon_end_model_path = 'models/moon_end.onnx'

        # Parameters
        self.odyssey_thresh = 10
        self.cap_end_thresh = 20
        self.moon_end_thresh = 20
        self.moon_end_blur_thresh = 1
        self.moon_count_thresh = 3

        self.moon_time = 0
        self.moon_values = []
        self.moon_min = 0
        self.moon_delay_done = False
        self.moon_count = 0

        self.kingdom_end = False
        self.moon_end = False
        self.end_checked = False

    def load_models(self, opts):
        self.odyssey_classifier = Classifier(self.odyssey_model_path, odyssey_prep, opts, self.odyssey_thresh)
        self.cap_end_classifier = Classifier(self.cap_end_model_path, cap_end_prep, opts, self.cap_end_thresh)
        self.moon_end_classifier = Classifier(self.moon_end_model_path, moon_end_prep, opts, self.moon_end_thresh)

    def update(self, frame, cap=False, odyssey=False, moon=False):
        self.kingdom_end = False

        # Odyssey Banner
        if odyssey:
            frame_prep = odyssey_prep.preprocess(frame).transpose((1, 2, 0))
            # Quick fix for false detections
            white_count = 0
            for i in range(12):
                if np.mean(frame_prep[0:2, i * 8:i * 8 + 8]) > 0.95:
                    white_count += 1

            if self.odyssey_classifier.update(frame) and white_count > 6:
                self.kingdom_end = True

        # Cap Kingdom
        if cap:
            if self.cap_end_classifier.update(frame):
                self.kingdom_end = True

        # Moon Kingdom
        if moon:
            if self.moon_end_classifier.update(frame) and not self.moon_end:
                self.moon_end = True
                self.moon_time = time.time()

            if self.moon_end_classifier.check_reset():
                self.moon_end = False
                self.moon_values = []
                self.moon_delay_done = False
                self.moon_count = 0

            if self.moon_end and time.time() > self.moon_time + 0.5:
                moon_blur = self.detect_blur_fft(frame, 20)
                if time.time() < self.moon_time + 3.5:
                    self.moon_values.append(moon_blur)

                if time.time() > self.moon_time + 3.5 and not self.moon_delay_done:
                    self.moon_delay_done = True
                    self.moon_min = np.asarray(self.moon_values).min()
                if time.time() > self.moon_time + 3.5 and moon_blur < self.moon_min - self.moon_end_blur_thresh:
                    self.moon_count += 1
                else:
                    self.moon_count = 0

                if self.moon_count >= self.moon_count_thresh:
                    self.moon_end = False
                    self.kingdom_end = True

        if not self.kingdom_end:
            self.end_checked = False

    def check_kingdom_end(self):
        if not self.end_checked and self.kingdom_end:
            self.end_checked = True
            return True
        else:
            return False

    @staticmethod
    def detect_blur_fft(image, size=60):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.resize(image, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
        (h, w) = image.shape
        (cX, cY) = (int(w / 2.0), int(h / 2.0))
        fft = np.fft.fft2(image)
        fft_shift = np.fft.fftshift(fft)

        fft_shift[cY - size:cY + size, cX - size:cX + size] = 0
        fft_shift = np.fft.ifftshift(fft_shift)
        recon = np.fft.ifft2(fft_shift)

        magnitude = 20 * np.log(np.abs(np.where(recon > 0, recon, 0.00001)))
        mean = np.mean(magnitude)

        return mean
