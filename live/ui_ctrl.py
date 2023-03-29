import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from danmuji_2 import Ui_MainWindow


class Danmuji(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.le_1.returnPressed.connect(lambda: self.ui.te_1.append(self.ui.le_1.text()))
        self.ui.maximize.clicked.connect(self.win_resize)
        self.show()

    def win_resize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.maximize.setIcon(QtGui.QIcon(":/top_menu/maximize.png"))
        else:
            self.showMaximized()
            self.ui.maximize.setIcon(QtGui.QIcon(":/top_menu/unmaximize.png"))

    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.mouse_click_left = True
            self.mouse_clicked_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, event) -> None:
        if QtCore.Qt.LeftButton and self.mouse_click_left:
            self.move(event.globalPos() - self.mouse_clicked_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.mouse_click_left = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


app = QtWidgets.QApplication(sys.argv)
ui = Danmuji()
sys.exit(app.exec_())
