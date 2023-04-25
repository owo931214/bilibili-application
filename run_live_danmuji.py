import sys
import threading

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from live.danmuji_ctrl import Danmuji
from live.socket import LiveSocket


class Thread(QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self, func, cls):
        super().__init__()
        self.cls = cls
        self.func = func

    def run(self):
        self.func(self.cls)
        self.finished.emit()


class Main(LiveSocket):
    def __init__(self, room_id=None, uid=None):
        super().__init__(room_id, uid)
        self.app = QApplication(sys.argv)
        self.danmuji = Danmuji()
        threading.Thread(target=self.app.exec_)
        self.start()

    def on_danmu(self):
        self.danmuji.append_msg(self.msg['uid'], self.msg['msg'])
        QApplication.processEvents()


if __name__ == "__main__":
    Main(room_id=675014)
