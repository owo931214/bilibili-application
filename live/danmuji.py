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
        MainWindow.resize(800, 560)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 781, 541))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.layout0_h0 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.layout0_h0.setContentsMargins(0, 0, 0, 0)
        self.layout0_h0.setObjectName("layout0_h0")
        self.layout1_v0 = QtWidgets.QVBoxLayout()
        self.layout1_v0.setObjectName("layout1_v0")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.layout1_v0.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.layout1_v0.addWidget(self.pushButton_3)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.layout1_v0.addWidget(self.pushButton)
        self.layout0_h0.addLayout(self.layout1_v0)
        self.layout1_v1 = QtWidgets.QVBoxLayout()
        self.layout1_v1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout1_v1.setSpacing(6)
        self.layout1_v1.setObjectName("layout1_v1")
        self.textEdit_2 = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit_2.setStyleSheet("font: 11pt \"Times New Roman\";")
        self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.layout1_v1.addWidget(self.textEdit_2)
        self.layout2_h0 = QtWidgets.QHBoxLayout()
        self.layout2_h0.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.layout2_h0.setObjectName("layout2_h0")
        self.timeEdit = QtWidgets.QTimeEdit(self.horizontalLayoutWidget)
        self.timeEdit.setStyleSheet("font: 11pt \"Times New Roman\";")
        self.timeEdit.setObjectName("timeEdit")
        self.layout2_h0.addWidget(self.timeEdit)
        self.dateEdit = QtWidgets.QDateEdit(self.horizontalLayoutWidget)
        self.dateEdit.setStyleSheet("font: 11pt \"Times New Roman\";")
        self.dateEdit.setObjectName("dateEdit")
        self.layout2_h0.addWidget(self.dateEdit)
        self.layout1_v1.addLayout(self.layout2_h0)
        self.layout0_h0.addLayout(self.layout1_v1)
        self.layout1_v2 = QtWidgets.QVBoxLayout()
        self.layout1_v2.setObjectName("layout1_v2")
        self.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEdit.setStyleSheet("font: 11pt \"Adobe 繁黑體 Std B\";")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.layout1_v2.addWidget(self.textEdit)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("font: 11pt \"Times New Roman\";")
        self.lineEdit.setObjectName("lineEdit")
        self.layout1_v2.addWidget(self.lineEdit)
        self.layout0_h0.addLayout(self.layout1_v2)
        self.layout0_h0.setStretch(0, 2)
        self.layout0_h0.setStretch(1, 5)
        self.layout0_h0.setStretch(2, 5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bilibili Live"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))