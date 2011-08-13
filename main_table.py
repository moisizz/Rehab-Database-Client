# -*- coding: utf8 -*-

from PyQt4 import QtCore,QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MainTable(QtGui.QTableWidget):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)
        self.setAutoFillBackground(True)
        self.setStyleSheet(_fromUtf8("#mainTable {background-color: rgb(248, 248, 209);}"))
        self.setFrameShadow(QtGui.QFrame.Sunken)
        self.setMidLineWidth(0)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setGridStyle(QtCore.Qt.SolidLine)
        self.setObjectName(_fromUtf8("mainTable"))
        
    def event(self, event):
        if (  
            (event.type()==QtCore.QEvent.KeyPress) and 
            ( (event.key() == QtCore.Qt.Key_C) and (event.modifiers() == QtCore.Qt.ControlModifier) )
           ):
            self.emit(QtCore.SIGNAL("copyPressed()"))
            return True

        return QtGui.QTableWidget.event(self, event)