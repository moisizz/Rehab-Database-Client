# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'arrive_form.ui'
#
# Created: Mon Jul 04 03:25:18 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(766, 566)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 8, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(180, 8, 31, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(310, 10, 46, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.leave_cause = QtGui.QLineEdit(Dialog)
        self.leave_cause.setGeometry(QtCore.QRect(310, 30, 320, 20))
        self.leave_cause.setObjectName(_fromUtf8("leave_cause"))
        self.arrive_date = QtGui.QDateEdit(Dialog)
        self.arrive_date.setGeometry(QtCore.QRect(56, 28, 110, 22))
        self.arrive_date.setCalendarPopup(True)
        self.arrive_date.setObjectName(_fromUtf8("arrive_date"))
        self.leave_date = QtGui.QDateEdit(Dialog)
        self.leave_date.setGeometry(QtCore.QRect(180, 28, 110, 22))
        self.leave_date.setCalendarPopup(True)
        self.leave_date.setObjectName(_fromUtf8("leave_date"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(15, 80, 741, 441))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.fotoArea = QtGui.QGraphicsView(self.groupBox)
        self.fotoArea.setGeometry(QtCore.QRect(100, 20, 631, 411))
        self.fotoArea.setObjectName(_fromUtf8("fotoArea"))
        self.makeFoto = QtGui.QPushButton(self.groupBox)
        self.makeFoto.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.makeFoto.setObjectName(_fromUtf8("makeFoto"))
        self.openFoto = QtGui.QPushButton(self.groupBox)
        self.openFoto.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.openFoto.setObjectName(_fromUtf8("openFoto"))
        self.saveButton = QtGui.QPushButton(Dialog)
        self.saveButton.setGeometry(QtCore.QRect(290, 530, 75, 23))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.deleteButton = QtGui.QPushButton(Dialog)
        self.deleteButton.setGeometry(QtCore.QRect(390, 530, 75, 23))
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.closeButton = QtGui.QPushButton(Dialog)
        self.closeButton.setGeometry(QtCore.QRect(490, 530, 75, 23))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.is_cure = QtGui.QCheckBox(Dialog)
        self.is_cure.setGeometry(QtCore.QRect(310, 60, 80, 17))
        self.is_cure.setObjectName(_fromUtf8("is_cure"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Прибытие/убытие", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Прибыл", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Убыл", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Причина", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Фото прибытия", None, QtGui.QApplication.UnicodeUTF8))
        self.makeFoto.setText(QtGui.QApplication.translate("Dialog", "Снять", None, QtGui.QApplication.UnicodeUTF8))
        self.openFoto.setText(QtGui.QApplication.translate("Dialog", "Открыть...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("Dialog", "Сохранить", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("Dialog", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Dialog", "Закрыть", None, QtGui.QApplication.UnicodeUTF8))
        self.is_cure.setText(QtGui.QApplication.translate("Dialog", "Долечился", None, QtGui.QApplication.UnicodeUTF8))

