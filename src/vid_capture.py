import logging
import time

import cv2

from PyQt5.QtMultimedia import QCameraInfo, QCamera
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class VideoCapture(QObject):
    sig_device_list_updated = pyqtSignal()

    instance = None
    initialized = False

    def __new__(cls):
        if VideoCapture.instance is None:
            VideoCapture.instance = super(VideoCapture, cls).__new__(cls)
        return VideoCapture.instance

    def __init__(self):
        super(VideoCapture, self).__init__()

        if not VideoCapture.initialized:
            VideoCapture.initialized = True
            self.device_list = {}
            self.capture_device = None
            self.device_list_worker = None

    def get_device_list(self):
        return self.device_list

    def update_device_list(self):
        self.device_list_worker = DeviceListWorker()
        self.device_list_worker.sig_device_list_updated.connect(self.device_list_updated)
        self.device_list_worker.start()

    def device_list_updated(self, device_list):
        self.device_list = device_list
        self.sig_device_list_updated.emit()
        print(self.device_list)

    def init_capture_device(self, index):
        if self.capture_device is not None:
            self.capture_device.release()

        try:
            capture_device = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        except Exception as e:
            logging.exception(e)
            return False

        if capture_device is None or not capture_device.isOpened():
            logging.error(f"Can't open capture device at index {index}")
            return False
        if not capture_device.grab():
            logging.error(f"Capture device at index {index} is already in use")
            return False

        try:
            # Set frame width
            capture_device.set(3, 640)
            # Set frame height
            capture_device.set(4, 480)
            # Set framerate
            capture_device.set(5, 60)
        except Exception as e:
            logging.exception(e)

        self.capture_device = capture_device
        return True

    def get_frame(self):
        if self.capture_device is None:
            time.sleep(0.01)
            return False, None

        try:
            retval, frame = self.capture_device.read()
        except Exception as e:
            logging.exception(e)
            return False, None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        return retval, frame

    def release(self):
        if self.capture_device is not None:
            self.capture_device.release()


class DeviceListWorker(QThread):
    sig_device_list_updated = pyqtSignal(dict)

    def __init__(self):
        QThread.__init__(self)

        self.device_list = {}

    def run(self):
        self.update_device_list()
        self.sig_device_list_updated.emit(self.device_list)

    def update_device_list(self):
        try:
            self.device_list.clear()
            index = 0
            for camera_info in QCameraInfo.availableCameras():
                self.device_list[str(index)] = camera_info.description()
                index += 1
        except Exception as e:
            logging.exception(e)
