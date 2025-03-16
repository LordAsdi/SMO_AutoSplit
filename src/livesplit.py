import datetime
import logging
import socket
import time
import re

from src.config import Config

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QThread


class Livesplit(QThread):
    sig_connection_status = pyqtSignal(bool)  # connected
    sig_connection_status2 = pyqtSignal(bool)  # connected
    sig_connection_status3 = pyqtSignal(bool)  # connected
    sig_timer_reset = pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

        self.connected = False
        self.connected2 = False
        self.connected3 = False

        self.port = Config.get_key("livesplit_port")
        self.port2_enabled = Config.get_key("livesplit_port2_enabled")
        self.port2 = Config.get_key("livesplit_port2")
        self.port3_enabled = Config.get_key("livesplit_port3_enabled")
        self.port3 = Config.get_key("livesplit_port3")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.prev_state = ""
        self.prev_read = 0
        self.read_interval = 0.2

        self.timer = datetime.timedelta(0, 0, 0, 0, 0, 0)
        self.final_timer = datetime.timedelta(0, 0, 0, 0, 0, 0)
        self.timer_phase = "NotRunning"

    def run(self):
        time.sleep(1)
        while True:
            if not self.connected:
                self.connect()
            else:
                self.check_connection()
                time.sleep(self.read_interval)
                self.check_reset()

            if self.port2_enabled:
                if not self.connected2:
                    self.connect2()
                else:
                    try:
                        self.socket2.send(bytes(b"") + b"\r\n")
                    except:
                        self.set_connection_status2(False)
                        self.socket2.close()
                        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if self.port3_enabled:
                if not self.connected3:
                    self.connect3()
                else:
                    try:
                        self.socket3.send(bytes(b"") + b"\r\n")
                    except:
                        self.set_connection_status3(False)
                        self.socket3.close()
                        self.socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            time.sleep(1 - self.read_interval)

    def check_connection(self):
        try:
            response = self.read(b"getcurrenttime")
        except Exception as e:
            pass
        else:
            if len(response) < 2:
                print("livesplit disconnected")
                self.set_connection_status(False)
                self.socket.close()
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                self.set_connection_status(True)

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
            self.set_connection_status(False)
        else:
            print("livesplit connected")
            self.set_connection_status(True)

    def connect2(self):
        try:
            self.socket2.connect(("localhost", self.port2))
        except Exception as e:
            self.set_connection_status2(False)
        else:
            self.set_connection_status2(True)
            print("livesplit port 2 connected")

    def connect3(self):
        try:
            self.socket3.connect(("localhost", self.port3))
        except Exception as e:
            self.set_connection_status3(False)
        else:
            self.set_connection_status3(True)
            print("livesplit port 3 connected")

    def set_connection_status(self, connected):
        self.connected = connected
        self.sig_connection_status.emit(connected)

    def set_connection_status2(self, connected):
        self.connected2 = connected
        self.sig_connection_status2.emit(connected)

    def set_connection_status3(self, connected):
        self.connected3 = connected
        self.sig_connection_status3.emit(connected)

    def send(self, cmd):
        try:
            self.socket.send(bytes(cmd) + b"\r\n")
            if self.connected2 and self.port2_enabled:
                self.socket2.send(bytes(cmd) + b"\r\n")
            if self.connected3 and self.port3_enabled:
                self.socket3.send(bytes(cmd) + b"\r\n")
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

    def reconnect_port(self):
        self.socket.close()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = Config.get_key("livesplit_port")
        self.set_connection_status(False)

    def reconnect_port2(self):
        self.socket2.close()
        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port2 = Config.get_key("livesplit_port2")
        self.port2_enabled = Config.get_key("livesplit_port2_enabled")
        self.set_connection_status2(False)

    def reconnect_port3(self):
        self.socket3.close()
        self.socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port3 = Config.get_key("livesplit_port3")
        self.port3_enabled = Config.get_key("livesplit_port3_enabled")
        self.set_connection_status3(False)
