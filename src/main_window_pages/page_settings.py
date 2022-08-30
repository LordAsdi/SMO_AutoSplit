import logging

from PyQt5.QtCore import QObject, pyqtSignal

from src.route_handler import RouteHandler
from src.vid_capture import VideoCapture
from src.config import Config


class PageSettings(QObject):
    sig_capture_device_changed = pyqtSignal(object)

    def __init__(self, ui):
        QObject.__init__(self)
        self.ui = ui
        self.vid_cap = VideoCapture()

        # Widgets
        self.check_updates_checkbox = self.ui.page_settings_checkbox_check_updates
        self.auto_update_checkbox = self.ui.page_settings_checkbox_auto_update
        self.capture_device_dropdown = self.ui.page_settings_dropdown_capture_device
        self.edit_crop_area_button = self.ui.page_settings_button_edit_crop_area

        self.check_updates_checkbox.checkbox.clicked.connect(self.check_updates_toggled)
        self.auto_update_checkbox.checkbox.clicked.connect(self.auto_update_toggled)

        # Load States From Config
        self.check_updates_checkbox.set_state(Config.get_key("check_for_updates"))
        self.auto_update_checkbox.set_state(Config.get_key("auto_update"))

    def device_list_updated(self):
        self.capture_device_dropdown.set_options(self.vid_cap.get_device_list())
        self.capture_device_dropdown.set_index(Config.get_key("capture_device"))
        self.capture_device_dropdown.dropdown.currentTextChanged.connect(self.capture_device_changed)

    def check_updates_toggled(self):
        Config.set_key("check_for_updates", self.check_updates_checkbox.get_state())
        Config.save_config()

    def auto_update_toggled(self):
        Config.set_key("auto_update", self.auto_update_checkbox.get_state())
        Config.save_config()

    def capture_device_changed(self):
        device_id = int(self.capture_device_dropdown.get_current_key())
        Config.set_key("capture_device", device_id)
        Config.save_config()
        self.sig_capture_device_changed.emit(device_id)
