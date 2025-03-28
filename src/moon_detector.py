import numpy as np
import time
import cv2

import src.classifiers.moon_get.preprocessing as get_prep
import src.classifiers.moon_count.preprocessing as count_prep
import src.classifiers.moon_multi_story.preprocessing as multi_prep
from src.classifiers.classifier import Classifier, NumericClassifier


class MoonDetector:
    def __init__(self):
        # Classifiers
        self.moon_get_classifier = None
        self.moon_count_classifier = None
        self.multi_story_classifier = None

        # Model Paths
        self.moon_get_model_path = 'models/moon_get.onnx'
        self.moon_count_model_path = 'models/moon_count.onnx'
        self.multi_story_model_path = 'models/multi_story.onnx'

        self.moon_get_thresh = 10
        self.moon_get_diff_thresh = 10
        self.moon_count_thresh = 5
        self.multi_story_thresh = 10

        self.moon_get_trigger = False
        self.moon_get_trigger_time = 0
        self.moon_get_time = 0
        self.moon_get_delay = 1.4
        self.moon_get_timeout = 1.8
        self.moon_get_pause = 1.5

        self.story_get_trigger = False
        self.story_delay = 3.0
        self.story_timeout = 3.5

        self.multi_get_time = 0
        self.multi_pause = 6.0
        self.multi_timeout = 3.5

        self.moon_tracker = cv2.legacy.TrackerMedianFlow.create()
        self.first_moon_count = -1
        self.prev_moon_frame = np.zeros((23, 12, 3), dtype="uint8")

        self.moon_get = False
        self.story_get = False
        self.multi_get = False

        self.moon_get_checked = False
        self.story_get_checked = False
        self.multi_get_checked = False

    def load_models(self, opts):
        self.moon_get_classifier = Classifier(self.moon_get_model_path, get_prep, opts, self.moon_get_thresh)
        self.moon_count_classifier = NumericClassifier(self.moon_count_model_path, count_prep, opts)
        self.multi_story_classifier = Classifier(self.multi_story_model_path, multi_prep, opts, self.multi_story_thresh)

    def update(self, frame, moon=False, story=False, multi=False):
        if moon:
            if time.time() > self.moon_get_time + self.moon_get_pause:
                if self.moon_get_classifier.update(frame):
                    if not self.moon_get_trigger:
                        self.moon_get_trigger_time = time.time()
                        self.moon_get_trigger = True
                        self.story_get_trigger = False
                        self.moon_get = False
                        self.story_get = False
                        self.first_moon_count = -1
                elif story and not self.story_get_trigger:
                    self.reset_moon_state()

        if story or multi:
            if self.multi_story_classifier.update(frame):
                if self.is_story(frame):
                    if not self.story_get_trigger:
                        self.moon_get_trigger_time = time.time()
                        self.story_get_trigger = True
                        self.moon_get_trigger = False
                        self.moon_get = False
                        self.story_get = False
                        self.first_moon_count = -1
                else:
                    if not self.multi_get and time.time() > self.multi_get_time + self.multi_pause:
                        self.multi_get = True
                        self.multi_get_checked = False
                        self.multi_get_time = time.time()
            elif (moon and not self.moon_get_trigger) or (self.multi_get and time.time() > self.multi_get_time + self.multi_pause + self.multi_timeout):
                self.reset_moon_state()

        if moon or story:
            if (self.moon_get_trigger and moon and time.time() > self.moon_get_trigger_time + self.moon_get_delay) or (
                    self.story_get_trigger and story and time.time() > self.moon_get_trigger_time + self.story_delay):
                if self.first_moon_count == -1:
                    self.moon_tracker.init(frame[61:61 + 23, 22:22 + 12], (1, 9, 10, 12))
                    self.first_moon_count = self.moon_count_classifier.update(frame)

                moon_frame = frame[61:61 + 23, 22:22 + 12]
                diff = cv2.absdiff(moon_frame, self.prev_moon_frame).mean()
                if not self.moon_get and not self.story_get:
                    moon_count = self.moon_count_classifier.update(frame)
                    if diff > self.moon_get_diff_thresh:
                        if not moon or self.moon_get_classifier.update(frame):
                            if self.first_moon_count == 0:
                                if moon_count == 1:
                                    self.set_moon_get(is_story=self.story_get_trigger)
                            elif 0 < self.first_moon_count < 20:
                                if moon_count == self.first_moon_count + 1:
                                    self.set_moon_get(is_story=self.story_get_trigger)
                            elif self.first_moon_count > 19:
                                ok, bbox = self.moon_tracker.update(moon_frame)
                                if moon_count == 20 and ok and int(bbox[1]) < 8:
                                    self.set_moon_get(is_story=self.story_get_trigger)

                self.prev_moon_frame = moon_frame

        if (self.moon_get_trigger and moon and time.time() > self.moon_get_trigger_time + self.moon_get_timeout) or (
                self.story_get_trigger and story and time.time() > self.moon_get_trigger_time + self.story_timeout):
            self.reset_moon_state()

    def is_story(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        th, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
        crop = img[253:253 + 41, 114:114 + 27]
        avg = crop.mean(axis=0).mean(axis=0)
        return avg > 128

    def set_moon_get(self, is_story=False):
        if is_story:
            self.story_get = True
            self.story_get_checked = False
        else:
            self.moon_get = True
            self.moon_get_checked = False
        self.moon_get_time = time.time()

    def reset_moon_state(self):
        self.moon_get_trigger = False
        self.story_get_trigger = False
        self.moon_get = False
        self.story_get = False
        self.multi_get = False
        self.moon_get_checked = False
        self.story_get_checked = False
        self.multi_get_checked = False
        self.first_moon_count = -1

    def check_moon_get(self):
        if not self.moon_get_checked:
            self.moon_get_checked = True
            return self.moon_get

    def check_storymoon_get(self):
        if not self.story_get_checked:
            self.story_get_checked = True
            return self.story_get

    def check_multimoon_get(self):
        if not self.multi_get_checked:
            self.multi_get_checked = True
            return self.multi_get
