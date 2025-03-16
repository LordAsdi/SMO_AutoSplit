import logging

from PyQt5.QtCore import QObject, pyqtSignal

from src.route_handler import RouteHandler
from src.vid_capture import VideoCapture
from src.config import Config


class PageSettings(QObject):
    sig_capture_device_changed = pyqtSignal(object)
    sig_livesplit_port_changed = pyqtSignal()
    sig_livesplit_port2_enabled_changed = pyqtSignal()
    sig_livesplit_port2_changed = pyqtSignal()
    sig_livesplit_port3_enabled_changed = pyqtSignal()
    sig_livesplit_port3_changed = pyqtSignal()

    def __init__(self, ui):
        QObject.__init__(self)
        self.ui = ui
        self.vid_cap = VideoCapture()

        # Widgets
        self.check_updates_checkbox = self.ui.page_settings_checkbox_check_updates
        self.auto_update_checkbox = self.ui.page_settings_checkbox_auto_update
        self.livesplit_port_input = self.ui.page_settings_livesplit_input_port
        self.livesplit_port_checkbox2 = self.ui.page_settings_livesplit_checkbox_port2
        self.livesplit_port_input2 = self.ui.page_settings_livesplit_input_port2
        self.livesplit_port_connected2 = self.ui.page_settings_livesplit_label_port2_connected
        self.livesplit_port_checkbox3 = self.ui.page_settings_livesplit_checkbox_port3
        self.livesplit_port_input3 = self.ui.page_settings_livesplit_input_port3
        self.livesplit_port_connected3 = self.ui.page_settings_livesplit_label_port3_connected
        self.capture_device_dropdown = self.ui.page_settings_dropdown_capture_device
        self.edit_crop_area_button = self.ui.page_settings_button_edit_crop_area

        self.check_updates_checkbox.checkbox.clicked.connect(self.check_updates_toggled)
        self.auto_update_checkbox.checkbox.clicked.connect(self.auto_update_toggled)
        self.livesplit_port_input.input_field.textEdited.connect(self.port_edited)
        self.livesplit_port_checkbox2.checkbox.clicked.connect(self.port_enabled_toggled2)
        self.livesplit_port_input2.input_field.textEdited.connect(self.port_edited2)
        self.livesplit_port_checkbox3.checkbox.clicked.connect(self.port_enabled_toggled3)
        self.livesplit_port_input3.input_field.textEdited.connect(self.port_edited3)

        # Load States From Config
        self.check_updates_checkbox.set_state(Config.get_key("check_for_updates"))
        self.auto_update_checkbox.set_state(Config.get_key("auto_update"))
        self.livesplit_port_input.set_text(str(Config.get_key("livesplit_port")))
        self.livesplit_port_checkbox2.set_state(Config.get_key("livesplit_port2_enabled"))
        self.livesplit_port_input2.set_text(str(Config.get_key("livesplit_port2")))
        self.livesplit_port_checkbox3.set_state(Config.get_key("livesplit_port3_enabled"))
        self.livesplit_port_input3.set_text(str(Config.get_key("livesplit_port3")))

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

    def port_edited(self):
        Config.set_key("livesplit_port", int(self.livesplit_port_input.get_text()))
        self.sig_livesplit_port_changed.emit()

    def port_enabled_toggled2(self):
        Config.set_key("livesplit_port2_enabled", self.livesplit_port_checkbox2.get_state())
        self.sig_livesplit_port2_enabled_changed.emit()

    def port_edited2(self):
        Config.set_key("livesplit_port2", int(self.livesplit_port_input2.get_text()))
        self.sig_livesplit_port2_changed.emit()

    def set_port2_connection_status(self, connected):
        if connected:
            self.livesplit_port_connected2.setText("Connected")
        else:
            self.livesplit_port_connected2.setText("Disconnected")

    def set_port3_connection_status(self, connected):
        if connected:
            self.livesplit_port_connected3.setText("Connected")
        else:
            self.livesplit_port_connected3.setText("Disconnected")

    def port_enabled_toggled3(self):
        Config.set_key("livesplit_port3_enabled", self.livesplit_port_checkbox3.get_state())
        self.sig_livesplit_port3_enabled_changed.emit()

    def port_edited3(self):
        Config.set_key("livesplit_port3", int(self.livesplit_port_input3.get_text()))
        self.sig_livesplit_port3_changed.emit()

    def capture_device_changed(self):
        device_id = int(self.capture_device_dropdown.get_current_key())
        Config.set_key("capture_device", device_id)
        Config.save_config()
        self.sig_capture_device_changed.emit(device_id)
