import datetime
import logging
import cv2
import os

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

from src.livesplit import Livesplit
from src.vid_capture import VideoCapture
from src.fps_counter import FpsCounter
from src.config import Config
from src.route_handler import RouteHandler

from src.start_detector import StartDetector
from src.moon_detector import MoonDetector
from src.kingdom_end_detector import KingdomEndDetector
from src.fadeout_detector import FadeoutDetector
from src.compass_detector import CompassDetector


class Autosplitter(QThread):
    sig_status_update = pyqtSignal(str, bool)  # message, busy
    sig_preview_update = pyqtSignal(QPixmap)  # preview image
    sig_preview_clear = pyqtSignal()
    sig_clear_splits = pyqtSignal()
    sig_add_splits = pyqtSignal(list)  # splits list
    sig_component_activated = pyqtSignal(int, int)  # activations, required activations
    sig_moon_count_changed = pyqtSignal(int, int)  # moon count, required moon count
    sig_component_changed = pyqtSignal(int)  # component index
    sig_next_split = pyqtSignal()
    sig_prev_split = pyqtSignal()
    sig_reset_splits = pyqtSignal()

    def __init__(self, parent_process):
        QThread.__init__(self)

        self.alive = True
        self.parent_process = parent_process
        self.running = False

        self.video_capture = VideoCapture()
        self.video_capture.update_device_list()
        self.video_capture.init_capture_device(Config.get_key("capture_device"))

        self.start_detector = StartDetector()
        self.moon_detector = MoonDetector()
        self.kingdom_end_detector = KingdomEndDetector()
        self.fadeout_detector = FadeoutDetector()
        self.compass_detector = CompassDetector()

        self.livesplit = Livesplit(16834)
        self.livesplit.sig_timer_reset.connect(self.reset_run)
        self.livesplit.start()

        self.fps_counter = FpsCounter(1, 60)
        self.fps_counter.start()

        self.current_split_index = 0
        self.current_split = None
        self.current_component_index = 0
        self.prev_component = None

        self.current_component = None
        self.moon_count = 0
        self.activations = 0
        self.run_started = False
        self.wait_for_reset = False

    def run(self):
        self.initialize()

        while self.alive:
            if self.running:
                self.update()
                self.fps_counter.update()

    def quit(self):
        self.alive = False
        self.video_capture.release()

        if self.livesplit.isRunning():
            self.livesplit.terminate()
            self.livesplit.wait()

        if self.fps_counter.isRunning():
            self.fps_counter.terminate()
            self.fps_counter.wait()

        if self.video_capture.device_list_worker.isRunning():
            self.video_capture.device_list_worker.terminate()
            self.video_capture.device_list_worker.wait()

    def initialize(self):

        self.sig_status_update.emit("Initializing ONNX Runtime", True)

        try:
            os.environ['OMP_NUM_THREADS'] = '1'

            import onnxruntime

            opts = onnxruntime.SessionOptions()
            opts.intra_op_num_threads = 1
            opts.inter_op_num_threads = 1
            opts.execution_mode = onnxruntime.ExecutionMode.ORT_SEQUENTIAL
        except Exception as e:
            logging.exception(e)
        else:
            self.sig_status_update.emit("Loading Models", True)
            self.moon_detector.load_models(opts)
            self.kingdom_end_detector.load_models(opts)
            self.fadeout_detector.load_models(opts)

        self.sig_status_update.emit("Done", False)

    @staticmethod
    def cv2_image_to_pixmap(image, width, height):
        if isinstance(image, type(None)) or image.shape[0] == 0 or image.shape[1] == 0 or image.shape[2] != 3:
            logging.warning(f"Image doesn't have correct shape. Expected (>0, >0, 3), got {image.shape}")
            return None

        try:
            image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            qimg = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
        except Exception as e:
            logging.exception(e)
            return None

        return pixmap

    def update(self):
        if self.current_component != self.prev_component:
            self.set_activations(self.activations)
            self.set_moon_count(self.moon_count)
            self.sig_component_changed.emit(self.current_component_index)
            self.prev_component = self.current_component

        retval, frame = self.video_capture.get_frame()
        if retval:
            if frame.shape[2] != 3:
                logging.warning(f"Expected frame to have 3 channels, got {frame.shape[2]}")
                return

            if frame.shape[0] != 480 or frame.shape[1] != 640:
                frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)

            width, height = self.parent_process.page_dashboard.get_preview_size()
            preview_pixmap = self.cv2_image_to_pixmap(frame, width, height)

            if preview_pixmap is None:
                self.sig_preview_clear.emit()
            else:
                self.sig_preview_update.emit(preview_pixmap)

            if RouteHandler.route is None:
                self.sig_status_update.emit("No route loaded", False)
                return
            elif RouteHandler.route.splits is None or len(RouteHandler.route.splits) == 0:
                self.sig_status_update.emit("Route has no splits", False)
                return
            else:
                if not self.livesplit.connected:
                    self.sig_status_update.emit("Livesplit not connected", False)
                    return
                if not self.run_started:
                    if self.wait_for_reset:
                        self.sig_status_update.emit("Waiting for livesplit to reset", True)
                        return

                    if RouteHandler.route.start_condition == "livesplit":
                        self.sig_status_update.emit("Waiting for livesplit to start", True)
                        timer = self.livesplit.get_timer()
                        if timer is not None and timer != datetime.timedelta(0, 0, 0, 0, 0, 0):
                            self.start_run()
                            print("Start")
                        return
                    elif RouteHandler.route.start_condition == "start_button":
                        self.sig_status_update.emit("Waiting for start button to be pressed", True)
                        self.start_detector.update(frame, start_button=True)
                        if self.start_detector.check_start_button():
                            self.start_run()
                            print("Start")
                        return
                    elif RouteHandler.route.start_condition == "time_date_ok_button":
                        self.sig_status_update.emit("Waiting for date and time ok button to be pressed", True)
                        self.start_detector.update(frame, date_time_ok=True)
                        if self.start_detector.check_date_time_ok():
                            self.start_run()
                            print("Start")
                        return

                if self.current_split is None:
                    if len(RouteHandler.route.splits) > 0:
                        try:
                            self.current_split = RouteHandler.route.splits[self.current_split_index]
                        except:
                            pass

                if self.current_split is None:
                    self.sig_status_update.emit("Route has no splits", True)

                if self.current_split is not None:
                    if self.current_component is None:
                        try:
                            self.current_component = self.current_split.components[self.current_component_index]
                        except:
                            pass

                    if self.current_component is None:
                        self.sig_status_update.emit("Current split has no components", True)

                    if self.current_component is not None:
                        if self.moon_count < self.current_component.min_moons:
                            self.sig_status_update.emit("Waiting for moon get", True)
                            self.moon_detector.update(frame, moon=True, story=True, multi=True)
                            if self.moon_detector.check_moon_get():
                                print("Moon Get")
                                self.set_moon_count(self.moon_count + 1)
                                print(f"Moon Count: {self.moon_count}")
                            elif self.moon_detector.check_storymoon_get():
                                print("Story Moon Get")
                                self.set_moon_count(self.moon_count + 1)
                                print(f"Moon Count: {self.moon_count}")
                            if self.moon_detector.check_multimoon_get():
                                print("Multi Moon Get")
                                self.set_moon_count(self.moon_count + 3)
                                print(f"Moon Count: {self.moon_count}")

                        else:
                            if self.current_component.name == "cap_end":
                                self.sig_status_update.emit("Waiting for cap kingdom end", True)
                                self.kingdom_end_detector.update(frame, cap=True)
                                if self.kingdom_end_detector.check_kingdom_end():
                                    self.component_activated()
                                    print("Cap End")
                            elif self.current_component.name == "odyssey":
                                self.sig_status_update.emit("Waiting for odyssey banner", True)
                                self.kingdom_end_detector.update(frame, odyssey=True)
                                if self.kingdom_end_detector.check_kingdom_end():
                                    self.component_activated()
                                    print("Odyssey")
                            elif self.current_component.name == "moon_end":
                                self.sig_status_update.emit("Waiting for moon kingdom end", True)
                                self.kingdom_end_detector.update(frame, moon=True)
                                if self.kingdom_end_detector.check_kingdom_end():
                                    self.component_activated()
                                    print("Moon End")
                            elif self.current_component.name == "world_map_fadeout":
                                self.sig_status_update.emit("Waiting for world map fadeout", True)
                                self.fadeout_detector.update(frame, world_map=True)
                                if self.fadeout_detector.check_world_map_fadeout():
                                    self.component_activated()
                                    print("World Map Fadeout")
                            elif self.current_component.name == "cutscene_skip":
                                self.sig_status_update.emit("Waiting for cutscene skip", True)
                                self.fadeout_detector.update(frame, cutscene=True)
                                if self.fadeout_detector.check_cutscene_fadeout():
                                    self.component_activated()
                                    print("Cutscene Skip")
                            elif self.current_component.name == "subarea":
                                self.sig_status_update.emit("Waiting for subarea fadeout", True)
                                self.fadeout_detector.update(frame, subarea=True)
                                if self.fadeout_detector.check_subarea_fadeout():
                                    self.component_activated()
                                    print("Subarea Fadeout")
                            elif self.current_component.name == "black_screen":
                                self.sig_status_update.emit("Waiting for black screen", True)
                                if self.fadeout_detector.check_black_screen(frame):
                                    self.component_activated()
                                    print("Black Screen")
                            elif self.current_component.name == "compass":
                                self.sig_status_update.emit("Waiting for compass disappear", True)
                                self.compass_detector.update(frame)
                                if self.compass_detector.check_compass():
                                    self.component_activated()
                                    print("Compass Disappear")
                            elif self.current_component.name == "moon_get":
                                self.sig_status_update.emit("Waiting for moon get", True)
                                self.moon_detector.update(frame, moon=True)
                                if self.moon_detector.check_moon_get():
                                    self.component_activated()
                                    print("Moon Get")
                            elif self.current_component.name == "moon_story":
                                self.sig_status_update.emit("Waiting for story moon get", True)
                                self.moon_detector.update(frame, story=True)
                                if self.moon_detector.check_storymoon_get():
                                    self.component_activated()
                                    print("Story Moon Get")
                            elif self.current_component.name == "moon_multi":
                                self.sig_status_update.emit("Waiting for multi moon get", True)
                                self.moon_detector.update(frame, multi=True)
                                if self.moon_detector.check_multimoon_get():
                                    self.component_activated()
                                    print("Multi Moon Get")

    def start_run(self):
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.livesplit.start_timer()
        self.run_started = True
        self.current_split_index = 0

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        self.current_component_index = 0

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_next_split.emit()

    def component_activated(self):
        print("Component Activated")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        if self.moon_count < self.current_component.min_moons:
            print(f"Min moon count not reached: {self.moon_count}/{self.current_component.min_moons}")

        self.set_activations(self.activations + 1)

        if self.activations >= self.current_component.activations:
            self.current_component_index += 1
            self.activations = 0

        if self.current_component_index >= len(self.current_split.components):
            self.next_split()
            return

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

    def next_split(self):
        if not self.run_started:
            return

        print("Next Split")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        if self.current_split.split:
            self.livesplit.split_timer()

        self.current_split_index += 1

        if self.current_split_index >= len(RouteHandler.route.splits):
            self.sig_next_split.emit()
            self.run_started = False
            self.wait_for_reset = True
            print("Run Finished")
            return

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        if self.current_split.reset_moon_count:
            self.moon_count = 0

        self.current_component_index = 0
        self.activations = 0

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_next_split.emit()

    def skip_split(self):
        if not self.run_started:
            return

        print("Skip Split")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.current_split_index += 1

        if self.current_split_index >= len(RouteHandler.route.splits):
            self.current_split_index = len(RouteHandler.route.splits) - 1
            return

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        if self.current_split.reset_moon_count:
            self.moon_count = 0

        self.current_component_index = 0
        self.activations = 0

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_next_split.emit()

    def undo_split(self):
        print("Undo Split")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.current_split_index -= 1

        if self.current_split_index < 0:
            self.current_component_index = 0
            return

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        self.current_component_index = 0
        self.activations = 0

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_prev_split.emit()

    def reset_run(self):
        print("Reset")
        self.current_split_index = 0
        self.current_split = None
        self.current_component_index = 0
        self.current_component = None
        self.moon_count = 0
        self.activations = 0
        self.run_started = False
        self.wait_for_reset = False
        self.sig_reset_splits.emit()

    def set_activations(self, value):
        self.activations = value
        if self.current_component is not None:
            self.sig_component_activated.emit(self.activations, self.current_component.activations)
            # print(f"Activations: {self.activations}/{self.current_component.activations}")

    def set_moon_count(self, value):
        self.moon_count = value
        if self.current_component is not None:
            self.sig_moon_count_changed.emit(self.moon_count, self.current_component.min_moons)
            # print(f"Moon Count: {self.moon_count}/{self.current_component.min_moons}")
