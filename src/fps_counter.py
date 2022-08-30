import time

from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class FpsCounter(QThread):
    sig_fps_update = QtCore.pyqtSignal(float)

    def __init__(self, interval, n_avgs=30):
        super().__init__()

        self.interval = interval
        self.n_avgs = n_avgs
        self.last_update = 0.0
        self.fps_hist = []
        self.fps = 0.0

    def run(self):
        while True:
            time.sleep(self.interval)
            self.sig_fps_update.emit(self.get_fps())

    def update(self):
        current_time = time.perf_counter()
        fps = 0
        try:
            fps = 1 / (current_time - self.last_update)
        except:
            pass
        self.fps_hist.append(fps)

        while len(self.fps_hist) > 0 and len(self.fps_hist) > self.n_avgs:
            self.fps_hist.pop(0)

        self.last_update = current_time

    def get_fps(self):
        if len(self.fps_hist) > 0:
            return sum(self.fps_hist) / len(self.fps_hist)
        else:
            return 0
