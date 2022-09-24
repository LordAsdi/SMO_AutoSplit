import datetime
import logging
import socket
import time
import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread


class Livesplit(QThread):
    sig_connection_status = pyqtSignal(bool)  # connected
    sig_timer_reset = pyqtSignal()

    def __init__(self, port):
        QThread.__init__(self)

        self.connected = False

        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.prev_state = ""
        self.prev_read = 0
        self.read_interval = 0.2

        self.timer = datetime.timedelta(0, 0, 0, 0, 0, 0)
        self.final_timer = datetime.timedelta(0, 0, 0, 0, 0, 0)
        self.timer_phase = "NotRunning"

    def run(self):
        while True:
            if not self.connected:
                self.connect()
            else:
                self.check_connection()
                time.sleep(self.read_interval)
                self.check_reset()
            time.sleep(1 - self.read_interval)

    def check_connection(self):
        try:
            response = self.read(b"getcurrenttime")
        except Exception as e:
            pass
        else:
            if len(response) < 2:
                print("livesplit disconnected")
                self.set_status(False)
                self.socket.close()
                time.sleep(0.5)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.set_status(True)

    def check_reset(self):
        state = self.get_timer_phase()
        if state == "NotRunning" and (self.prev_state == "Running" or self.prev_state == "Ended"):
            self.timer = datetime.timedelta(0, 0, 0, 0, 0, 0)
            self.sig_timer_reset.emit()
        self.prev_state = state

    def connect(self):
        try:
            self.socket.connect(("localhost", self.port))
        except Exception as e:
            # logging.exception(e)
            self.set_status(False)
            time.sleep(0.5)
        else:
            print("livesplit connected")
            self.set_status(True)

    def set_status(self, connected):
        self.connected = connected
        self.sig_connection_status.emit(connected)

    def send(self, cmd):
        try:
            self.socket.send(bytes(cmd) + b"\r\n")
        except Exception as e:
            logging.warning("LiveSplit command send failed")
            logging.exception(e)

    def read(self, cmd):
        self.prev_read = time.time()
        try:
            self.socket.send(bytes(cmd) + b"\r\n")
            self.socket.settimeout(10)
            response = self.socket.recv(1024).decode("utf-8").strip()
            return response
        except Exception as e:
            logging.warning("LiveSplit command send failed")
            logging.exception(e)
            return ""

    @staticmethod
    def parse_timer(time_string):
        try:
            split_response = re.split(r'[:.]', time_string)
            split_response = [int(x) for x in split_response]

            if time_string.count(':') == 0:
                seconds, milliseconds = split_response
                timer = datetime.timedelta(seconds=seconds,
                                           milliseconds=milliseconds * 10)
                return timer
            if time_string.count(':') == 1:
                minutes, seconds, milliseconds = split_response
                timer = datetime.timedelta(minutes=minutes,
                                           seconds=seconds,
                                           milliseconds=milliseconds * 10)
                return timer
            elif time_string.count(':') == 2:
                hours, minutes, seconds, milliseconds = split_response
                timer = datetime.timedelta(hours=hours,
                                           minutes=minutes,
                                           seconds=seconds,
                                           milliseconds=milliseconds * 10)
                return timer
            else:
                return None
        except Exception as e:
            logging.exception(e)
            return None

    def start_timer(self):
        self.send(b"starttimer")

    def split_timer(self):
        self.send(b"split")

    def reset_timer(self):
        self.send(b"reset")

    def get_timer(self):
        if time.time() > self.prev_read + self.read_interval:
            response = self.read(b"getcurrenttime")
            self.timer = self.parse_timer(response)
        return self.timer

    def get_final_timer(self):
        if time.time() > self.prev_read + self.read_interval:
            response = self.read(b"getfinaltime")
            self.final_timer = self.parse_timer(response)
        return self.final_timer

    def get_timer_phase(self):
        if time.time() > self.prev_read + self.read_interval:
            self.timer_phase = self.read(b"getcurrenttimerphase")
        return self.timer_phase
