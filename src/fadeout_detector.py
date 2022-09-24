import numpy as np
import time
import cv2

import src.classifiers.subarea.preprocessing as subarea_prep
import src.classifiers.cutscene.preprocessing as cutscene_prep
from src.classifiers.classifier import Classifier


class FadeoutDetector:
    def __init__(self):
        # Classifiers
        self.subarea_classifier = None
        self.cutscene_classifier = None

        # Model Paths
        self.subarea_model_path = 'models/subarea.onnx'
        self.cutscene_model_path = 'models/cutscene.onnx'

        self.world_map_vals = []
        self.world_map_fadeout = False
        self.cutscene_detected = False
        self.cutscene_fadeout = False
        self.cutscene_fadeout_checked = False
        self.subarea_detected = False
        self.subarea_fadeout = False
        self.subarea_fadeout_checked = False
        self.black_screen = False
        self.black_screen_checked = False
        self.white_screen = False
        self.white_screen_checked = False
        self.last_fadeout = time.time()

        # Parameters
        self.scale = 0.2
        self.world_map_sum_thresh = 5000 * self.scale
        self.world_map_dist_thresh = 10 * self.scale
        self.avg_setpoint = np.asarray([50 * self.scale, 50 * self.scale, 0, 0])
        self.med_setpoint = np.asarray([55 * self.scale, 55 * self.scale, 0, 0])
        self.subarea_thresh = 10
        self.cutscene_thresh = 5
        self.black_screen_avg_thresh = 8
        self.black_screen_std_thresh = 2
        self.white_screen_avg_thresh = 235
        self.white_screen_std_thresh = 2
        self.fadeout_cooldown = 0.5

    def load_models(self, opts):
        self.subarea_classifier = Classifier(self.subarea_model_path, subarea_prep, opts, self.subarea_thresh)
        self.cutscene_classifier = Classifier(self.cutscene_model_path, cutscene_prep, opts, self.cutscene_thresh)

    def update(self, frame, world_map=False, cutscene=False, subarea=False):
        timestamp = time.time()
        cv2.rectangle(frame, (21, 442), (171, 465), (0, 0, 0), -1)
        frame_res = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LINEAR)
        frame_bw = cv2.cvtColor(frame_res, cv2.COLOR_RGB2GRAY)

        # World Map fadeout
        if world_map:
            frame_world_map_v = frame_bw[0:int(240 * self.scale), :]
            world_map_sum = np.sum(frame_world_map_v, axis=1)

            n_black = 0
            for val in world_map_sum:
                if val < self.world_map_sum_thresh:
                    n_black += 1

            self.world_map_vals.append([timestamp, n_black])

            while len(self.world_map_vals) > 70:
                self.world_map_vals.pop(0)

        # Cutscene fadeout
        if cutscene:
            if self.cutscene_classifier.update(frame):
                self.cutscene_detected = True

            if self.cutscene_classifier.check_reset():
                self.cutscene_detected = False
                self.cutscene_fadeout = False
                self.cutscene_fadeout_checked = False

            if self.cutscene_detected and self.check_black_screen(frame):
                self.cutscene_detected = False
                self.cutscene_fadeout = True

        # Subarea fadeout
        if subarea:
            if self.subarea_classifier.update(frame):
                self.subarea_detected = True

            if self.subarea_classifier.check_reset():
                self.subarea_detected = False
                self.subarea_fadeout = False
                self.subarea_fadeout_checked = False

            if self.subarea_detected and self.check_black_screen(frame):
                self.subarea_detected = False
                self.subarea_fadeout = True

    def check_world_map_fadeout(self):
        if len(self.world_map_vals) < 60:
            self.world_map_fadeout = False
            return False

        avg_dist = 0
        start_time = self.world_map_vals[-1][0] - 1
        n_samples = 0

        for i in range(0, 61):
            sample = self.world_map_vals[-i]
            if sample[0] < start_time:
                continue
            avg_dist += self.get_sample_dist(self.world_map_poly, sample[0] - start_time, sample[1])
            n_samples += 1
        avg_dist /= n_samples

        if self.world_map_vals[-1][1] == 240 * self.scale and avg_dist < self.world_map_dist_thresh:
            if not self.world_map_fadeout and time.time() > self.last_fadeout + self.fadeout_cooldown:
                self.world_map_fadeout = True
                self.last_fadeout = time.time()
                return True
            else:
                return False

        self.world_map_fadeout = False
        return False

    def check_cutscene_fadeout(self):
        if self.cutscene_fadeout and not self.cutscene_fadeout_checked:
            self.cutscene_fadeout_checked = True
            return True
        else:
            return False

    def check_subarea_fadeout(self):
        if self.subarea_fadeout and not self.subarea_fadeout_checked:
            self.subarea_fadeout_checked = True
            return True
        else:
            return False

    def check_black_screen(self, frame):
        cv2.rectangle(frame, (21, 442), (171, 465), (0, 0, 0), -1)
        frame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        avg = np.average(frame_bw)
        std_dev = np.std(frame_bw)

        if avg < self.black_screen_avg_thresh and std_dev < self.black_screen_std_thresh:
            self.black_screen = True
        else:
            self.black_screen = False
            self.black_screen_checked = False

        if self.black_screen and not self.black_screen_checked:
            self.black_screen_checked = True
            return True
        else:
            return False

    def check_white_screen(self, frame):
        cv2.rectangle(frame, (21, 442), (171, 465), (255, 255, 255), -1)
        frame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        avg = np.average(frame_bw)
        std_dev = np.std(frame_bw)

        if avg > self.white_screen_avg_thresh and std_dev < self.white_screen_std_thresh:
            self.white_screen = True
        else:
            self.white_screen = False
            self.white_screen_checked = False

        if self.white_screen and not self.white_screen_checked:
            self.white_screen_checked = True
            return True
        else:
            return False

    def world_map_poly(self, x):
        return (0.0006 * (x * 60) ** 3 - 0.1402 * (x * 60) ** 2 + 10.427 * (x * 60) - 10.718) * self.scale

    def get_sample_dist(self, polynomial, x, y):
        return abs(polynomial(x) - y)
