# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'danmuji.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(-1, -1, 301, 801))
        self.frame.setStyleSheet("border: none;\n"
"                        background-color: rgba(255, 255, 255, 0);\n"
"                        font: 24pt \"Adobe Gothic Std B\";\n"
"                    ")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.te = QtWidgets.QTextEdit(self.frame)
        self.te.setStyleSheet("")
        self.te.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te.setReadOnly(True)
        self.te.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.te.setObjectName("te")
        self.verticalLayout.addWidget(self.te)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
