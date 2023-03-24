from danmuji import Ui_MainWindow
import sys
from PyQt5 import QtWidgets

class danmuji(Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(MainWindow)
        self.lineEdit.editingFinished.connect(lambda: self.textEdit.append(self.lineEdit.text()))
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = danmuji()
MainWindow.show()
sys.exit(app.exec_())