import logging
import sys
import os

from PyQt5.QtCore import QObject, QSize, Qt, QPoint, QEvent, QTimer, QRect
from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QApplication, QSizeGrip, QPushButton

from src.config import Config
from ui.main_window_ui import MainWindowUi
from ui.styles import Style
from src.autosplitter import Autosplitter
from src.cpu_monitor import CpuMonitor
from src.route_handler import RouteHandler
from ui.popup_ui import UpdateAvailablePopup
from updater import Updater

from src.main_window_pages.page_dashboard import PageDashboard
from src.main_window_pages.page_route import PageRoute
from src.main_window_pages.page_settings import PageSettings


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.page_title = "Dashboard"
        self.fullscreen = False
        self.restore_size = None
        self.sizegrip = None

        # Start update check
        self.update_available = False
        self.update = False
        self.update_popup = None
        self.updater = None
        if Config.get_key("check_for_updates"):
            self.updater = Updater()
            self.updater.sig_update_check.connect(self.update_check_done)
            self.updater.check_for_update()

        # Set up ui
        self.ui = MainWindowUi()
        self.ui.close_callback = self.exit
        self.ui.setup_ui()
        self.setup_frameless_window()

        self.ui.setWindowTitle("SMO AutoSplit")
        self.ui.setWindowIcon(QIcon('ui/resources/icons/icon.ico'))

        # Set up required classes
        self.autosplitter = Autosplitter(self)

        self.page_dashboard = PageDashboard(self.ui, self.autosplitter)
        self.page_route = PageRoute(self.ui)
        self.page_settings = PageSettings(self.ui)

        self.cpu_monitor = CpuMonitor(1)
        self.cpu_monitor.sig_cpu_usage_update.connect(self.set_cpu_usage)
        self.cpu_monitor.start()

        # Connect Signals
        self.ui.page_dashboard_close_route_btn.clicked.connect(RouteHandler.close_route_btn)
        self.ui.page_dashboard_load_route_btn.clicked.connect(RouteHandler.load_route_btn)
        self.ui.page_dashboard_save_route_btn.clicked.connect(RouteHandler.save_route_btn)
        self.ui.page_dashboard_save_route_as_btn.clicked.connect(RouteHandler.save_route_as_btn)

        self.ui.page_route_close_route_btn.clicked.connect(RouteHandler.close_route_btn)
        self.ui.page_route_load_route_btn.clicked.connect(RouteHandler.load_route_btn)
        self.ui.page_route_save_route_btn.clicked.connect(RouteHandler.save_route_btn)
        self.ui.page_route_save_route_as_btn.clicked.connect(RouteHandler.save_route_as_btn)

        self.page_route.sig_route_modified.connect(self.page_dashboard.route_updated)

        self.autosplitter.sig_status_update.connect(self.set_status)
        self.autosplitter.sig_preview_update.connect(self.page_dashboard.update_preview)
        self.autosplitter.sig_preview_clear.connect(self.page_dashboard.clear_preview)
        self.autosplitter.sig_clear_splits.connect(self.page_dashboard.clear_splits)
        self.autosplitter.sig_add_splits.connect(self.page_dashboard.add_splits)
        self.autosplitter.sig_component_activated.connect(self.page_dashboard.component_activated)
        self.autosplitter.sig_moon_count_changed.connect(self.page_dashboard.moon_count_changed)
        self.autosplitter.sig_component_changed.connect(self.page_dashboard.component_changed)
        self.autosplitter.sig_next_split.connect(self.page_dashboard.next_split)
        self.autosplitter.sig_prev_split.connect(self.page_dashboard.prev_split)
        self.autosplitter.sig_reset_splits.connect(self.page_dashboard.reset_splits)
        self.autosplitter.livesplit.sig_connection_status.connect(self.set_livesplit_status)
        self.autosplitter.fps_counter.sig_fps_update.connect(self.set_fps)
        self.autosplitter.video_capture.sig_device_list_updated.connect(self.page_settings.device_list_updated)

        # Add menus
        self.add_menu("Dashboard", "btn_dashboard", "ui/resources/icons/home.png", is_top_menu=True)
        self.add_menu("Route", "btn_route", "ui/resources/icons/map.png", is_top_menu=True)
        self.add_menu("Settings", "btn_settings", "ui/resources/icons/settings.png", is_top_menu=False)
        self.ui.layout_menu_bottom.addWidget(self.ui.frame_menu_spacer)

        self.select_standard_menu("btn_dashboard")

        # Load version
        self.ui.label_version.setText("v" + ''.join([x for x in Config.version if not x.isalpha()]))
        if "b" not in Config.version:
            self.ui.label_beta.parent().layout().removeWidget(self.ui.label_beta)
            self.ui.label_beta.deleteLater()

        # Load window position
        window_pos = Config.get_key("window_position")
        if window_pos is not None:
            self.ui.move(window_pos[0], window_pos[1])

        # Load window size
        try:
            width, height = Config.get_key("window_size")
            self.ui.resize(width, height)
        except Exception as e:
            logging.exception(e)
            self.ui.resize(1000, 724)

        # Load current route
        def update_routes():
            self.page_dashboard.route_updated()
            self.page_route.route_updated()
            self.set_title()

        RouteHandler.route_updated = update_routes
        RouteHandler.load_route(Config.get_key("current_route"))

        # Start autosplitter
        self.autosplitter.start()
        self.autosplitter.running = True

        # Set current page
        self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_dashboard)

        self.set_title()

        self.ui.show()

        self.recenter_ui()

        if Config.get_key("fullscreen"):
            self.maximize_restore()

    def button(self):
        btn_widget = self.sender()

        if btn_widget.objectName() == "btn_dashboard":
            self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_dashboard)
            self.page_title = "Dashboard"

        if btn_widget.objectName() == "btn_route":
            self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_route)
            self.page_title = "Route"

        if btn_widget.objectName() == "btn_settings":
            self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_settings)
            self.page_title = "Settings"

        self.reset_style(btn_widget.objectName())
        self.set_title()
        btn_widget.setStyleSheet(self.select_menu(btn_widget.styleSheet()))

    def add_menu(self, name, obj_name, icon, is_top_menu):
        button = QPushButton(self.ui)
        button.setObjectName(obj_name)
        button.setFixedSize(QSize(55, 55))
        button.setStyleSheet(Style.btn_tabs)
        button.setToolTip(name)
        button.setIcon(QIcon(QPixmap(icon)))
        button.setIconSize(QSize(23, 23))
        button.clicked.connect(self.button)

        if is_top_menu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    @staticmethod
    def select_menu(get_style):
        select = get_style + "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
        return select

    @staticmethod
    def deselect_menu(get_style):
        deselect = get_style.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    def select_standard_menu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(self.select_menu(w.styleSheet()))

    def reset_style(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(self.deselect_menu(w.styleSheet()))

    def set_title(self):
        if RouteHandler.route is not None:
            self.ui.label_title_bar_top.setText(f"{self.page_title} - {RouteHandler.route.name}")
        else:
            self.ui.label_title_bar_top.setText(self.page_title)

    def set_status(self, msg, busy=False):
        self.ui.label_status.setText(msg)
        self.ui.label_status.adjustSize()
        if busy:
            self.ui.status_busy_anim.start()
        else:
            self.ui.status_busy_anim.stop()
            self.ui.status_busy_anim.jumpToFrame(0)

    def set_livesplit_status(self, connected):
        if connected:
            self.ui.label_livesplit_status.setText("Connected")
            self.ui.label_livesplit_status.adjustSize()
            self.ui.label_livesplit_status.setStyleSheet("color: rgb(91, 153, 61);")
        else:
            self.ui.label_livesplit_status.setText("Disconnected")
            self.ui.label_livesplit_status.adjustSize()
            self.ui.label_livesplit_status.setStyleSheet("color: rgb(153, 61, 61);")

    def set_cpu_usage(self, usage):
        self.ui.label_cpu_usage_percent.setText(f"{usage:.1f}%")
        self.ui.label_cpu_usage_percent.adjustSize()

    def set_fps(self, fps):
        self.ui.label_fps_value.setText(f"{fps:.1f}")
        self.ui.label_fps_value.adjustSize()

    def exit(self):
        self.ui.close()

        if self.cpu_monitor.isRunning():
            self.cpu_monitor.terminate()
            self.cpu_monitor.wait()

        self.autosplitter.quit()

        if self.autosplitter.isRunning():
            self.autosplitter.terminate()
            self.autosplitter.wait()

        if self.updater.worker.isRunning():
            self.updater.worker.terminate()
            self.updater.worker.wait()

        import time
        time.sleep(0.1)

        if self.update_available and self.update:
            self.updater.apply_update()

    def setup_frameless_window(self):
        self.ui.setWindowFlags(Qt.FramelessWindowHint)

        def double_click_maximize_restore(event):
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: self.maximize_restore())

        self.ui.frame_label_top_btns.mouseDoubleClickEvent = double_click_maximize_restore

        def move_window(event):
            if self.fullscreen:
                self.maximize_restore()
                self.ui.move(self.ui.dragPos - QPoint(int(self.ui.width() / 2), 10))

            if event.buttons() == Qt.LeftButton:
                self.ui.move(self.ui.pos() + event.globalPos() - self.ui.dragPos)
                self.ui.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = move_window

        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 25px; height: 25px; margin: 0px; background-color: transparent;")

        self.ui.btn_minimize.clicked.connect(lambda: self.ui.showMinimized())
        self.ui.btn_maximize_restore.clicked.connect(lambda: self.maximize_restore())
        self.ui.btn_close.clicked.connect(lambda: self.ui.close())

    def maximize_restore(self):
        if not self.fullscreen:
            self.restore_size = self.ui.size()
            self.ui.showMaximized()
            self.fullscreen = True
            self.ui.btn_maximize_restore.setIcon(QIcon(QPixmap("ui/resources/icons/fullscreen_exit.png")))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.setToolTip("Restore")
        else:
            self.fullscreen = False
            self.ui.showNormal()
            self.ui.resize(self.restore_size)
            self.ui.btn_maximize_restore.setIcon(QIcon(QPixmap("ui/resources/icons/fullscreen.png")))
            self.ui.frame_size_grip.show()
            self.ui.btn_maximize_restore.setToolTip("Maximize")

    def get_screen_corners(self):
        desktop = app.desktop()
        screens = []
        for i in range(desktop.screenCount()):
            rect = desktop.availableGeometry(i)
            screens.append((rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()))
        return screens

    def is_on_screen(self, x, y):
        screens = self.get_screen_corners()
        on_screen = False
        for screen in screens:
            if not on_screen and screen[0] < x < screen[2] and screen[1] < y < screen[3]:
                on_screen = True
        return on_screen

    def recenter_ui(self):
        sr = self.ui.window().windowHandle().screen().availableGeometry()
        fr = self.ui.frameSize()
        cwr = QRect(QPoint(), fr.boundedTo(sr.size()))
        pos = self.ui.pos()

        if not self.is_on_screen(pos.x(), pos.y()) or not self.is_on_screen(pos.x() + fr.width(), pos.y()) or \
                not self.is_on_screen(pos.x(), pos.y() + fr.height()) or \
                not self.is_on_screen(pos.x() + fr.width(), pos.y() + fr.height()):
            self.ui.resize(cwr.size())
            self.ui.move(sr.center() - cwr.center())

    def update_check_done(self, value):
        self.update_available = value

        if value and not Config.get_key("auto_update"):
            self.update_popup = UpdateAvailablePopup(self.updater.worker.app_update.version)
            self.update_popup.sig_clicked_yes.connect(self.update_popup_yes)
            self.update_popup.sig_clicked_no.connect(self.update_popup_no)
            self.update_popup.show()
        else:
            self.update = True

    def update_popup_yes(self):
        self.update = True

    def update_popup_no(self):
        self.update = False


def load_fonts():
    QFontDatabase.addApplicationFont("ui/resources/fonts/moon_get-Heavy.ttf")
    QFontDatabase.addApplicationFont("ui/resources/fonts/Roboto-Light.ttf")
    QFontDatabase.addApplicationFont("ui/resources/fonts/Roboto-Medium.ttf")
    QFontDatabase.addApplicationFont("ui/resources/fonts/Roboto-Regular.ttf")
    QFontDatabase.addApplicationFont("ui/resources/fonts/Roboto-Bold.ttf")
    QFontDatabase.addApplicationFont("ui/resources/fonts/Roboto-Black.ttf")
    QFontDatabase.addApplicationFont("ui/resources/fonts/Raleway-Black.ttf")


if __name__ == "__main__":
    print("main")

    # Clear log
    appdata = os.path.join(os.path.expandvars(r'%LOCALAPPDATA%'), "Lord Asdi", "SMO AutoSplit")
    log_path = os.path.join(appdata, "application.log")
    os.makedirs(appdata, exist_ok=True)
    try:
        with open(log_path, 'w'):
            pass
    except:
        pass

    logging.basicConfig(filename=log_path,
                        format="\n%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s\n\n",
                        level=logging.DEBUG)

    # Console Logging
    # console = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d - %(message)s')
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)

    Config.init()

    app = QApplication(sys.argv)
    load_fonts()
    print("fonts loaded")
    window = MainWindow()
    print("MainWindow constructed")
    exit_code = app.exec_()
    print(f"Exit Code: {exit_code}")
    sys.exit(exit_code)
