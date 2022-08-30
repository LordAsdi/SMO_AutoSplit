import os
import time
import psutil

from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class CpuMonitor(QThread):
    sig_cpu_usage_update = QtCore.pyqtSignal(float)

    def __init__(self, interval):
        QThread.__init__(self)

        self.interval = interval

        self.psutil = psutil.Process(os.getpid())
        self.cpu_hist = []

    def run(self):
        self.psutil.cpu_percent(interval=None)
        while True:
            time.sleep(self.interval)
            self.update()
            self.sig_cpu_usage_update.emit(self.get_cpu_usage())

    def update(self):
        usage = self.psutil.cpu_percent(interval=None)
        self.cpu_hist.append(usage / psutil.cpu_count())
        while len(self.cpu_hist) > 1:
            self.cpu_hist.pop(0)

    def get_cpu_usage(self):
        if len(self.cpu_hist) > 0:
            return sum(self.cpu_hist) / len(self.cpu_hist)
