import logging
import re

from pyupdater.client import Client
from lib.utils.client_config import ClientConfig

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ui.updater_ui import UpdaterUi
from src.config import Config


class Updater(QObject):
    sig_update_check = pyqtSignal(bool)

    def __init__(self):
        super(Updater, self).__init__()
        self.ui = UpdaterUi()
        self.ui.sig_closed.connect(self.done)
        self.worker = UpdateWorker()
        self.worker.sig_done.connect(self.done)
        self.worker.sig_progress.connect(self.progress_report)

        self.ui.set_status(self.ui.Status.downloading)

    def apply_update(self):
        self.worker.set_task(self.worker.Task.apply_update)
        self.ui.initialize()
        self.ui.show()
        self.worker.start()

    def done(self):
        if self.worker.task == self.worker.Task.update_check:
            update_available = self.worker.app_update is not None and self.worker.app_update.version != ""
            if update_available:
                self.ui.set_download_version(self.worker.app_update.version)
                self.ui.set_status(self.ui.Status.downloading)
                print(self.worker.app_update.data_dir)
                print("Update Available")
            self.sig_update_check.emit(update_available)
        elif self.worker.task == self.worker.Task.apply_update:
            self.ui.close()
            exit(0)

    def check_for_update(self):
        self.worker.set_task(self.worker.Task.update_check)
        self.worker.start()

    def progress_report(self, percentage, status):
        self.ui.set_progress(percentage)
        if status == "finished":
            self.ui.set_status(self.ui.Status.installing)
        else:
            self.ui.set_status(self.ui.Status.downloading)


class UpdateWorker(QThread):
    sig_done = pyqtSignal()
    sig_progress = pyqtSignal(float, object)

    class Task:
        update_check = 0
        apply_update = 1

    def __init__(self):
        super(UpdateWorker, self).__init__()

        self.client = Client(ClientConfig(), refresh=False, progress_hooks=[self.report_progress])
        self.app_update = None
        self.task = None

    def report_progress(self, info):
        total = info.get(u'total')
        downloaded = info.get(u'downloaded')
        percentage = downloaded / total * 100
        status = info.get(u'status')
        self.sig_progress.emit(percentage, status)
        print(status, percentage)

    def set_task(self, task):
        self.task = task

    def run(self, **kwargs):
        try:
            self.client.refresh()
        except Exception as e:
            logging.exception(e)
            return

        if self.task == self.Task.update_check:
            self.check_for_update()
        elif self.task == self.Task.apply_update:
            if self.app_update is None:
                self.check_for_update()
            self.download_update()
            print("Done downloading")
            self.install_update()

        print("Updater Worker Done")
        self.sig_done.emit()

    def check_for_update(self):
        print(Config.version)
        version = re.sub(r'[^Z0-9_.]+', '', Config.version)
        print(f"Version: {version}")
        try:
            self.app_update = self.client.update_check(ClientConfig.APP_NAME, version, channel="stable")
        except Exception as e:
            logging.exception(e)
            return

    def download_update(self):
        if self.app_update is not None:
            print("Downloading Update")
            try:
                self.app_update.download()
            except Exception as e:
                logging.exception(e)
                return
        else:
            print("No update")
            return

    def install_update(self):
        if self.app_update.is_downloaded():
            print("Installing Update")
            try:
                self.app_update.extract_overwrite()
                print("Done Installing")
            except Exception as e:
                logging.exception(e)
                return
        else:
            print("Update not downloaded")
            return


def update_check_done(value):
    print(f"Update check {value}")


if __name__ == '__main__':
    import sys

    Config.init()

    app = QApplication(sys.argv)
    updater = Updater()
    updater.sig_update_check.connect(update_check_done)
    updater.check_for_update()
    sys.exit(app.exec_())
