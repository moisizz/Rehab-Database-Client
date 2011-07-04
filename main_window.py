# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Sun Jul 03 23:07:54 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(900, 535)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(3, 1, 891, 491))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.mainLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.mainLayout.setMargin(0)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.buttonBar = QtGui.QHBoxLayout()
        self.buttonBar.setObjectName(_fromUtf8("buttonBar"))
        self.openButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.openButton.setEnabled(False)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.buttonBar.addWidget(self.openButton)
        self.addButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.addButton.setEnabled(False)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.buttonBar.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.buttonBar.addWidget(self.deleteButton)
        self.filterButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.filterButton.setEnabled(False)
        self.filterButton.setObjectName(_fromUtf8("filterButton"))
        self.buttonBar.addWidget(self.filterButton)
        self.mainLayout.addLayout(self.buttonBar)
        self.mainTable = QtGui.QTableWidget(self.verticalLayoutWidget)
        self.mainTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.mainTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.mainTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.mainTable.setGridStyle(QtCore.Qt.SolidLine)
        self.mainTable.setObjectName(_fromUtf8("mainTable"))
        self.mainTable.setColumnCount(0)
        self.mainTable.setRowCount(0)
        self.mainLayout.addWidget(self.mainTable)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.openBaseAction = QtGui.QAction(MainWindow)
        self.openBaseAction.setObjectName(_fromUtf8("openBaseAction"))
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName(_fromUtf8("exitAction"))
        self.createBaseAction = QtGui.QAction(MainWindow)
        self.createBaseAction.setObjectName(_fromUtf8("createBaseAction"))
        self.menu.addAction(self.createBaseAction)
        self.menu.addAction(self.openBaseAction)
        self.menu.addSeparator()
        self.menu.addAction(self.exitAction)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.exitAction, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Новый свет - База данных", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("MainWindow", "Открыть", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("MainWindow", "Добавить", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("MainWindow", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.filterButton.setText(QtGui.QApplication.translate("MainWindow", "Фильтр", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTable.setSortingEnabled(True)
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.openBaseAction.setText(QtGui.QApplication.translate("MainWindow", "Открыть базу...", None, QtGui.QApplication.UnicodeUTF8))
        self.exitAction.setText(QtGui.QApplication.translate("MainWindow", "Выход", None, QtGui.QApplication.UnicodeUTF8))
        self.createBaseAction.setText(QtGui.QApplication.translate("MainWindow", "Создать пустую базу...", None, QtGui.QApplication.UnicodeUTF8))

