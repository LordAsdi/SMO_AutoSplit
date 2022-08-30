from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from ui.styles import Style
from ui.colors import Color
from ui.fonts import *


class UnsavedChangesPopup(QWidget):
    sig_clicked_yes = pyqtSignal()
    sig_clicked_no = pyqtSignal()
    sig_clicked_cancel = pyqtSignal()
    sig_closed = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)

        self.yes = False
        self.no = False
        self.cancel = False

        self.setStyleSheet(f"background-color: {Color.background};")
        self.setWindowTitle("Save Route?")

        self.label = QLabel("Your route has been modified but not yet saved.\nDo you want to save your route now?")
        self.label.setStyleSheet(f"color: {Color.text_white}; background-color: {Color.background}; padding: 20px;")
        self.label.setFont(font_10pt)

        self.button_yes = QPushButton("Yes")
        self.button_yes.setStyleSheet(Style.btn_centered)
        self.button_yes.setFixedWidth(100)
        self.button_yes.setFont(font_10pt)
        self.button_yes.clicked.connect(self.yes_btn_click)

        self.button_no = QPushButton("No")
        self.button_no.setStyleSheet(Style.btn_centered)
        self.button_no.setFixedWidth(100)
        self.button_no.setFont(font_10pt)
        self.button_no.clicked.connect(self.no_btn_click)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setStyleSheet(Style.btn_centered)
        self.button_cancel.setFixedWidth(100)
        self.button_cancel.setFont(font_10pt)
        self.button_cancel.clicked.connect(self.cancel_btn_click)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.button_yes)
        button_layout.addWidget(self.button_no)
        button_layout.addWidget(self.button_cancel)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(11)
        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

    def showEvent(self, event):
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                self.resize(0, 0)
                geo = self.geometry()
                geo.moveCenter(widget.geometry().center())
                self.setGeometry(geo)
        event.accept()

    def closeEvent(self, event):
        event.accept()
        if not self.yes and not self.no and not self.cancel:
            self.sig_closed.emit()

    def yes_btn_click(self):
        self.sig_clicked_yes.emit()
        self.yes = True
        self.close()

    def no_btn_click(self):
        self.sig_clicked_no.emit()
        self.no = True
        self.close()

    def cancel_btn_click(self):
        self.sig_clicked_cancel.emit()
        self.cancel = True
        self.close()


class RouteLoadFailedPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setStyleSheet(f"background-color: {Color.background};")
        self.setWindowTitle("Save Route?")

        self.label = QLabel("The file you selected is not a valid route.")
        self.label.setStyleSheet(f"color: {Color.text_white}; background-color: {Color.background}; padding: 20px;")
        self.label.setFont(font_10pt)

        self.button_ok = QPushButton("Ok")
        self.button_ok.setStyleSheet(Style.btn_centered)
        self.button_ok.setFixedWidth(100)
        self.button_ok.setFont(font_10pt)
        self.button_ok.clicked.connect(self.ok_btn_click)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.button_ok)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(11)
        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

    def showEvent(self, event):
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                self.resize(0, 0)
                geo = self.geometry()
                geo.moveCenter(widget.geometry().center())
                self.setGeometry(geo)
        event.accept()

    def ok_btn_click(self):
        self.close()


class RouteSaveWarningPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setStyleSheet(f"background-color: {Color.background};")
        self.setWindowTitle("Save Route?")

        self.label = QLabel(
            "Files saved in the SMO AutoSplit directory will\nget overwritten when an update is installed!")
        self.label.setStyleSheet(f"color: {Color.text_white}; background-color: {Color.background}; padding: 20px;")
        self.label.setFont(font_10pt)

        self.button_ok = QPushButton("Ok")
        self.button_ok.setStyleSheet(Style.btn_centered)
        self.button_ok.setFixedWidth(100)
        self.button_ok.setFont(font_10pt)
        self.button_ok.clicked.connect(self.ok_btn_click)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.button_ok)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(11)
        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

    def showEvent(self, event):
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                self.resize(0, 0)
                geo = self.geometry()
                geo.moveCenter(widget.geometry().center())
                self.setGeometry(geo)
        event.accept()

    def ok_btn_click(self):
        self.close()


class UpdateAvailablePopup(QWidget):
    sig_clicked_yes = pyqtSignal()
    sig_clicked_no = pyqtSignal()
    sig_closed = pyqtSignal()

    def __init__(self, version):
        QWidget.__init__(self)

        self.yes = False
        self.no = False
        self.cancel = False

        self.setStyleSheet(f"background-color: {Color.background};")
        self.setWindowTitle("Save Route?")

        self.label = QLabel(
            f"There is a newer version available: {version}.\nDo you want to update after closing the application?")
        self.label.setStyleSheet(f"color: {Color.text_white}; background-color: {Color.background}; padding: 20px;")
        self.label.setFont(font_10pt)

        self.button_yes = QPushButton("Yes")
        self.button_yes.setStyleSheet(Style.btn_centered)
        self.button_yes.setFixedWidth(100)
        self.button_yes.setFont(font_10pt)
        self.button_yes.clicked.connect(self.yes_btn_click)

        self.button_no = QPushButton("No")
        self.button_no.setStyleSheet(Style.btn_centered)
        self.button_no.setFixedWidth(100)
        self.button_no.setFont(font_10pt)
        self.button_no.clicked.connect(self.no_btn_click)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(self.button_yes)
        button_layout.addWidget(self.button_no)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(11)
        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(button_widget)

        self.setLayout(main_layout)

    def showEvent(self, event):
        app = QApplication.instance()
        for widget in app.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                self.resize(0, 0)
                geo = self.geometry()
                geo.moveCenter(widget.geometry().center())
                self.setGeometry(geo)
        event.accept()

    def closeEvent(self, event):
        event.accept()
        if not self.yes and not self.no:
            self.sig_closed.emit()

    def yes_btn_click(self):
        self.sig_clicked_yes.emit()
        self.yes = True
        self.close()

    def no_btn_click(self):
        self.sig_clicked_no.emit()
        self.no = True
        self.close()
