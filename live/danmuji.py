# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\User\Downloads\bilibili-application-master\live\danmuji.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

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
"background-color: rgba(255, 255, 255, 0);\n"
"font: 24pt \"Adobe Gothic Std B\";")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pte = QtWidgets.QPlainTextEdit(self.frame)
        self.pte.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pte.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pte.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.pte.setReadOnly(True)
        self.pte.setPlainText("")
        self.pte.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.pte.setMaximumBlockCount(10)
        self.pte.setObjectName("pte")
        self.verticalLayout.addWidget(self.pte)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

