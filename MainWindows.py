# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(602, 523)
        self.rec_knn = QtWidgets.QPushButton(Dialog)
        self.rec_knn.setGeometry(QtCore.QRect(370, 40, 131, 25))
        self.rec_knn.setObjectName("rec_knn")
        self.Exit = QtWidgets.QPushButton(Dialog)
        self.Exit.setGeometry(QtCore.QRect(370, 120, 131, 21))
        self.Exit.setObjectName("Exit")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(80, 40, 271, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(80, 100, 271, 241))
        self.textEdit.setObjectName("textEdit")
        self.rec_svd = QtWidgets.QPushButton(Dialog)
        self.rec_svd.setGeometry(QtCore.QRect(370, 80, 131, 25))
        self.rec_svd.setObjectName("rec_svd")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 20, 241, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 80, 201, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(80, 360, 201, 17))
        self.label_3.setObjectName("label_3")
        self.img = QtWidgets.QLabel(Dialog)
        self.img.setGeometry(QtCore.QRect(80, 390, 455, 67))
        self.img.setText("")
        self.img.setObjectName("img")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.rec_knn.setText(_translate("Dialog", "knn_recommend"))
        self.Exit.setText(_translate("Dialog", "Exit"))
        self.rec_svd.setText(_translate("Dialog", "svd_recommend"))
        self.label.setText(_translate("Dialog", "Input the movie you are interested"))
        self.label_2.setText(_translate("Dialog", "The recommendation result"))
        self.label_3.setText(_translate("Dialog", "Posters"))


