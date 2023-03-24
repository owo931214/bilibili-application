import sys

from PyQt5 import QtWidgets

from danmuji_2 import Ui_MainWindow


class Danmuji(Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(MainWindow)
        self.lineEdit.returnPressed.connect(lambda: self.textEdit.append(self.lineEdit.text()))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Danmuji()
MainWindow.show()
sys.exit(app.exec_())
