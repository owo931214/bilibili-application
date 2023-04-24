import sys
import threading

from PyQt5.QtWidgets import QApplication

from live.danmuji_ctrl import Danmuji
from live.socket import LiveSocket


class Main(LiveSocket):
    def __init__(self, room_id=None, uid=None):
        super().__init__(room_id, uid)
        self.app = QApplication(sys.argv)
        self.danmuji = Danmuji()
        self.danmuji.append_msg(self.uid, "彈幕機已開啟")
        self.ui_thread = threading.Thread(target=self.start)
        self.ui_thread.start()
        sys.exit(self.app.exec_())

    def on_danmu(self):
        self.danmuji.append_msg(self.msg['uid'], self.msg['msg'])


if __name__ == "__main__":
    Main(room_id=22320946)
