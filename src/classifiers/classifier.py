import numpy as np
import onnxruntime
import logging
import time


class Classifier:
    def __init__(self, model_path, preprocessing, opts, threshold):
        self.model = self.load_model(model_path, opts)
        self.preprocessing = preprocessing
        self.threshold = threshold

        self.count = 0
        self.prev_update = time.time()

    @staticmethod
    def load_model(model_path, opts):
        print(f"Loading Model {model_path}")
        try:
            return onnxruntime.InferenceSession(model_path, sess_options=opts)
        except Exception as e:
            logging.warning(f"Failed to load model \"{model_path}\"")
            logging.exception(e)
            return None

    def update(self, frame):
        # Reset after 1 second of inactivity
        if time.time() - self.prev_update > 1:
            self.count = 0
        self.prev_update = time.time()

        frame_prep = self.preprocessing.preprocess(frame)
        inputs = {self.model.get_inputs()[0].name: np.expand_dims(frame_prep, axis=0).astype('float32')}
        pred = np.argmax(self.model.run(None, inputs)[0], axis=1)[0]

        if pred == 1:
            if self.count < 0:
                self.count = 0
            else:
                self.count += 1
        else:
            if self.count > 0:
                self.count = 0
            else:
                self.count -= 1

        self.count = np.clip(self.count, -self.threshold, self.threshold)
        return self.count >= self.threshold

    def check_reset(self):
        return self.count <= -self.threshold


class NumericClassifier:
    def __init__(self, model_path, preprocessing, opts):
        self.model = self.load_model(model_path, opts)
        self.preprocessing = preprocessing

    @staticmethod
    def load_model(model_path, opts):
        print(f"Loading Model {model_path}")
        try:
            return onnxruntime.InferenceSession(model_path, sess_options=opts)
        except Exception as e:
            logging.warning(f"Failed to load model \"{model_path}\"")
            logging.exception(e)
            return None

    def update(self, frame):
        frame_prep = self.preprocessing.preprocess(frame)
        inputs = {self.model.get_inputs()[0].name: frame_prep.astype('float32')}
        pred = np.argmax(self.model.run(None, inputs)[0], axis=1).sum()

        return pred
