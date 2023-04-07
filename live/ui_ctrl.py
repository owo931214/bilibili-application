import sys
import time
from utils.converter import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow

from live.danmuji import Ui_MainWindow

color_list = ["#ff0000", "#ff4d00", "#ff8400", "#ffae00", "#ffd500", "#c8ff00", "#a2ff00", "#40ff00", "#00ff8c", "#00ffbf", "#00ffea", "#00a6ff",
              "#007bff", "#0062ff", "#0040ff", "#001aff", "#0d00ff", "#2b00ff", "#4800ff", "#6200ff", "#8000ff", "#9d00ff", "#ff0055", "#ff0033"]


class Danmuji(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()
        self.color_index = 0
        self.mouse_click_left = False
        self.mouse_clicked_pos = None
        self.ui.te.setAlignment(Qt.AlignBottom)
        self.append_msg("11111111111111111111111111111111111111111111111111")
        QApplication.processEvents()
        for i in range(20):
            self.append_msg(i)
            QApplication.processEvents()
            time.sleep(0.5)

    def append_msg(self, msg):
        # self.ui.te.insertHtml(f"""
        #     <div style="display: flex, inline; align-items: flex-start;">
        #         <img src="data:image/png;base64,{uid2face(1).decode()}" style="border-radius: 50%;margin-right: 10px; align-self: flex-start;">
        #         <p style="color: {color_list[self.color_index]}; display: flex; flex-direction: column; align-items: flex-start; margin: 0;
        #         text-align: justify;">{msg}</p>
        #     </div>
        # """)
        self.ui.te.insertHtml(f"""
                    <img src="data:image/png;base64,{uid2face(1).decode()}" style="border-radius: 50%;margin-right: 10px; align-self: flex-start;">
                    </div>
                """)
        self.color_index += 1
        if self.color_index == len(color_list):
            self.color_index = 0

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and not self.isMaximized():
            self.mouse_click_left = True
            self.mouse_clicked_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event) -> None:
        if Qt.LeftButton and self.mouse_click_left:
            self.move(event.globalPos() - self.mouse_clicked_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.mouse_click_left = False
        self.setCursor(QCursor(Qt.ArrowCursor))


app = QApplication(sys.argv)
ui = Danmuji()
sys.exit(app.exec_())
