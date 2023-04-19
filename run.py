# time_start = time.time()
# wsapp = LiveSocket(room_id=768756)  # 4767523 沙月, 22320946 純寶, 4141795 小沙月, 768756 滋蹦, 24393 雪狐
# print(time.time() - time_start)
import sys

from PyQt5.QtWidgets import QApplication

from live.ui_ctrl import Danmuji

app = QApplication(sys.argv)
ui = Danmuji()
ui.msg_test()
sys.exit(app.exec_())
