import sys
import threading

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from utils.converter import *
from live.danmuji_ctrl import Danmuji
from live.socket import LiveSocket


class Main(LiveSocket):
    def __init__(self, room_id=None, uid=None):
        super().__init__(room_id, uid)
        self.face = {}
        self.app = QApplication(sys.argv)
        self.danmuji = Danmuji()
        threading.Thread(target=self.app.exec_)
        self.start()

    def on_danmu(self):
        def function():
            if self.msg['uid'] not in self.face:
                self.face.update({
                    self.msg['uid']: uid2face(self.msg['uid'])
                })
            self.danmuji.append_msg(f"""
                    <img src="data:image/png;base64,{face_decompress(self.face[self.msg['uid']])}" width="50" height="50">{str(self.msg['msg'])}
                """)
            QApplication.processEvents()
        threading.Thread(target=function).start()


if __name__ == "__main__":
    Main(room_id=13829253)
