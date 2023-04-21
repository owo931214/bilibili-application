import sys
from live.socket import LiveSocket
from live.ui_ctrl import Danmuji
from PyQt5.QtWidgets import QApplication


class Main(LiveSocket):
    def __init__(self, room_id=None, uid=None):
        super().__init__(room_id, uid)
        self.danmuji = Danmuji()
        self.start()

    def on_danmu(self):
        self.danmuji.append_msg(self.msg['uid'], self.msg['msg'])


app = QApplication(sys.argv)
Main(uid=128912828)