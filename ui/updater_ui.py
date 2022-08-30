from PyQt5.QtGui import QMovie

from ui.custom_widgets import *


class UpdaterUi(QMainWindow):
    sig_closed = pyqtSignal()

    class Status:
        downloading = 0
        installing = 1

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.width = 300
        self.height = 70
        self.setWindowIcon(QIcon('ui/resources/icons/icon.ico'))
        self.setWindowTitle("SMO AutoSplit Updater")

        self._version = ""
        self.status = self.Status.downloading

        self.main_layout = QVBoxLayout()

        self.content_widget = QWidget()
        self.label = QLabel("")
        self.label_busy_anim = QLabel(self)
        self.busy_anim = QMovie("ui/resources/icons/load_anim.gif")
        self.progress_bar = QProgressBar()
        self.progress_widget = QWidget()
        self.progress_layout = QHBoxLayout()

    def initialize(self):
        self.setFixedSize(self.width, self.height)
        self.setCentralWidget(self.content_widget)

        self.progress_widget.setLayout(self.progress_layout)

        self.progress_bar.setFixedSize(250, 20)
        self.label_busy_anim.setFixedSize(24, 32)

        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.label_busy_anim.setMovie(self.busy_anim)
        self.busy_anim.setScaledSize(QSize(24, 24))
        self.busy_anim.start()

        self.progress_layout.setContentsMargins(0, 0, 0, 0)
        self.progress_layout.addWidget(self.label_busy_anim)
        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addStretch()

        abort_button_container = QWidget()
        abort_button_container.setLayout(QVBoxLayout())
        abort_button_container.layout().setContentsMargins(0, 0, 0, 0)
        abort_button_container.layout().addStretch(0)
        abort_button_container.layout().setSpacing(0)

        self.content_widget.setLayout(QVBoxLayout())
        self.content_widget.layout().addWidget(self.label)
        self.content_widget.layout().addWidget(self.progress_widget)
        self.content_widget.layout().addWidget(abort_button_container, alignment=QtCore.Qt.AlignRight)

    def set_download_version(self, version):
        self._version = version
        self.set_status(self.status)

    def set_status(self, status):
        self.status = status
        if self.status == self.Status.downloading:
            self.label.setText(f"Downloading Version {self._version}")
        elif self.status == self.Status.installing:
            self.label.setText(f"Installing Version {self._version}")

    def set_progress(self, percent):
        self.progress_bar.setValue(int(percent))

    def display_error_message(self, message, title="Error"):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.show()

    def closeEvent(self, event):
        self.sig_closed.emit()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = UpdaterUi()
    sys.exit(app.exec_())
