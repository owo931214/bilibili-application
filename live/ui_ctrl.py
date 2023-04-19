import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow

from live.danmuji import Ui_MainWindow
from utils.converter import *

color_list = ["#ff0000", "#ff4d00", "#ff8400", "#ffae00", "#ffd500", "#c8ff00", "#a2ff00", "#40ff00", "#00ff8c", "#00ffbf", "#00ffea", "#00a6ff",
              "#007bff", "#0062ff", "#0040ff", "#001aff", "#0d00ff", "#2b00ff", "#4800ff", "#6200ff", "#8000ff", "#9d00ff", "#ff0055", "#ff0033"]


# uid = 690121705
class Danmuji(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.face = {}
        self.color_index = 0
        self.mouse_click_left = False
        self.mouse_clicked_pos = None
        self.textedit = self.ui.te
        self.textedit_cursor = self.textedit.textCursor()
        self.textedit_document = self.textedit.document()
        self.ui.te.setAlignment(Qt.AlignBottom)
        for i in range(20):
            self.textedit_cursor.insertBlock()
        self.textedit.ensureCursorVisible()
        self.show()

    def append_msg(self, uid, msg):
        if uid not in self.face:
            self.face.update({
                uid: uid2face(uid)
            })
        self.textedit_cursor.insertBlock()
        self.textedit_cursor.insertHtml(f"""
            <p style="color: {color_list[self.color_index]};">
                <img src="data:image/png;base64,{face_decompress(self.face[uid])}"
                width=30 style="border-radius: 30px;">
                {str(msg)}
             </p>
        """)
        self.textedit.moveCursor(self.textedit_cursor.End)
        self.textedit.ensureCursorVisible()
        self.color_index += 1
        if self.color_index == len(color_list):
            self.color_index = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isMaximized():
            self.mouse_click_left = True
            self.mouse_clicked_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.mouse_click_left:
            self.move(event.globalPos() - self.mouse_clicked_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.mouse_click_left = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def msg_test(self):
        for i in range(25):
            self.append_msg(24992412, i)
            QApplication.processEvents()
            time.sleep(0.1)
