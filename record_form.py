# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'record_form.ui'
#
# Created: Tue Jul 12 01:22:14 2011
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
        Dialog.resize(864, 537)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/user")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.mainBox = QtGui.QGroupBox(Dialog)
        self.mainBox.setGeometry(QtCore.QRect(0, 0, 477, 532))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBox.sizePolicy().hasHeightForWidth())
        self.mainBox.setSizePolicy(sizePolicy)
        self.mainBox.setMinimumSize(QtCore.QSize(477, 532))
        self.mainBox.setMaximumSize(QtCore.QSize(477, 532))
        self.mainBox.setTitle(_fromUtf8(""))
        self.mainBox.setFlat(False)
        self.mainBox.setObjectName(_fromUtf8("mainBox"))
        self.passpor_group = QtGui.QGroupBox(self.mainBox)
        self.passpor_group.setGeometry(QtCore.QRect(16, 155, 440, 71))
        self.passpor_group.setObjectName(_fromUtf8("passpor_group"))
        self.label_6 = QtGui.QLabel(self.passpor_group)
        self.label_6.setGeometry(QtCore.QRect(10, 18, 70, 13))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.passport_given = QtGui.QLineEdit(self.passpor_group)
        self.passport_given.setGeometry(QtCore.QRect(151, 38, 281, 20))
        self.passport_given.setObjectName(_fromUtf8("passport_given"))
        self.label_8 = QtGui.QLabel(self.passpor_group)
        self.label_8.setGeometry(QtCore.QRect(150, 20, 46, 13))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.passport = QtGui.QLineEdit(self.passpor_group)
        self.passport.setGeometry(QtCore.QRect(10, 38, 131, 20))
        self.passport.setInputMask(_fromUtf8(""))
        self.passport.setText(_fromUtf8(""))
        self.passport.setObjectName(_fromUtf8("passport"))
        self.last_name = QtGui.QLineEdit(self.mainBox)
        self.last_name.setGeometry(QtCore.QRect(25, 70, 131, 20))
        self.last_name.setObjectName(_fromUtf8("last_name"))
        self.label_11 = QtGui.QLabel(self.mainBox)
        self.label_11.setGeometry(QtCore.QRect(30, 282, 101, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.notes = QtGui.QPlainTextEdit(self.mainBox)
        self.notes.setGeometry(QtCore.QRect(32, 420, 411, 71))
        self.notes.setTabChangesFocus(True)
        self.notes.setObjectName(_fromUtf8("notes"))
        self.label_7 = QtGui.QLabel(self.mainBox)
        self.label_7.setGeometry(QtCore.QRect(320, 97, 87, 13))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.born_place = QtGui.QLineEdit(self.mainBox)
        self.born_place.setGeometry(QtCore.QRect(317, 117, 131, 20))
        self.born_place.setObjectName(_fromUtf8("born_place"))
        self.label_12 = QtGui.QLabel(self.mainBox)
        self.label_12.setGeometry(QtCore.QRect(186, 282, 78, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.first_name = QtGui.QLineEdit(self.mainBox)
        self.first_name.setGeometry(QtCore.QRect(165, 70, 140, 20))
        self.first_name.setObjectName(_fromUtf8("first_name"))
        self.label_3 = QtGui.QLabel(self.mainBox)
        self.label_3.setGeometry(QtCore.QRect(317, 55, 51, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.closeButton = QtGui.QPushButton(self.mainBox)
        self.closeButton.setGeometry(QtCore.QRect(370, 500, 90, 23))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.contact_person = QtGui.QLineEdit(self.mainBox)
        self.contact_person.setGeometry(QtCore.QRect(186, 302, 261, 20))
        self.contact_person.setInputMask(_fromUtf8(""))
        self.contact_person.setObjectName(_fromUtf8("contact_person"))
        self.label_4 = QtGui.QLabel(self.mainBox)
        self.label_4.setGeometry(QtCore.QRect(170, 97, 84, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.deleteButton = QtGui.QPushButton(self.mainBox)
        self.deleteButton.setGeometry(QtCore.QRect(29, 500, 75, 23))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete_person")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon1)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.label_5 = QtGui.QLabel(self.mainBox)
        self.label_5.setGeometry(QtCore.QRect(30, 235, 87, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.saveButton = QtGui.QPushButton(self.mainBox)
        self.saveButton.setGeometry(QtCore.QRect(270, 500, 90, 23))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/add_person")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.label_15 = QtGui.QLabel(self.mainBox)
        self.label_15.setGeometry(QtCore.QRect(33, 403, 63, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label = QtGui.QLabel(self.mainBox)
        self.label.setGeometry(QtCore.QRect(166, 55, 20, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.middle_name = QtGui.QLineEdit(self.mainBox)
        self.middle_name.setGeometry(QtCore.QRect(316, 70, 131, 20))
        self.middle_name.setObjectName(_fromUtf8("middle_name"))
        self.gender = QtGui.QGroupBox(self.mainBox)
        self.gender.setGeometry(QtCore.QRect(20, 97, 141, 47))
        self.gender.setFlat(False)
        self.gender.setCheckable(False)
        self.gender.setObjectName(_fromUtf8("gender"))
        self.female = QtGui.QRadioButton(self.gender)
        self.female.setGeometry(QtCore.QRect(60, 18, 50, 17))
        self.female.setObjectName(_fromUtf8("female"))
        self.male = QtGui.QRadioButton(self.gender)
        self.male.setGeometry(QtCore.QRect(10, 17, 50, 17))
        self.male.setChecked(True)
        self.male.setObjectName(_fromUtf8("male"))
        self.born_date = QtGui.QDateEdit(self.mainBox)
        self.born_date.setGeometry(QtCore.QRect(170, 117, 134, 22))
        self.born_date.setCalendarPopup(True)
        self.born_date.setObjectName(_fromUtf8("born_date"))
        self.contact_phone = QtGui.QLineEdit(self.mainBox)
        self.contact_phone.setGeometry(QtCore.QRect(32, 302, 141, 20))
        self.contact_phone.setInputMask(_fromUtf8(""))
        self.contact_phone.setObjectName(_fromUtf8("contact_phone"))
        self.addiction_group = QtGui.QGroupBox(self.mainBox)
        self.addiction_group.setGeometry(QtCore.QRect(20, 330, 431, 61))
        self.addiction_group.setObjectName(_fromUtf8("addiction_group"))
        self.addiction_start_date = QtGui.QDateEdit(self.addiction_group)
        self.addiction_start_date.setGeometry(QtCore.QRect(223, 22, 71, 22))
        self.addiction_start_date.setCalendarPopup(True)
        self.addiction_start_date.setObjectName(_fromUtf8("addiction_start_date"))
        self.label_10 = QtGui.QLabel(self.addiction_group)
        self.label_10.setGeometry(QtCore.QRect(170, 26, 50, 13))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.addiction_id = QtGui.QComboBox(self.addiction_group)
        self.addiction_id.setGeometry(QtCore.QRect(36, 22, 110, 22))
        self.addiction_id.setObjectName(_fromUtf8("addiction_id"))
        self.label_14 = QtGui.QLabel(self.addiction_group)
        self.label_14.setGeometry(QtCore.QRect(13, 26, 20, 13))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.label_2 = QtGui.QLabel(self.mainBox)
        self.label_2.setGeometry(QtCore.QRect(30, 55, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.address = QtGui.QLineEdit(self.mainBox)
        self.address.setGeometry(QtCore.QRect(30, 255, 416, 20))
        self.address.setObjectName(_fromUtf8("address"))
        self.contract_number = QtGui.QLineEdit(self.mainBox)
        self.contract_number.setGeometry(QtCore.QRect(26, 25, 131, 20))
        self.contract_number.setObjectName(_fromUtf8("contract_number"))
        self.label_9 = QtGui.QLabel(self.mainBox)
        self.label_9.setGeometry(QtCore.QRect(30, 9, 68, 13))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.arriveTable = QtGui.QTableWidget(Dialog)
        self.arriveTable.setGeometry(QtCore.QRect(488, 4, 373, 219))
        self.arriveTable.setStyleSheet(_fromUtf8("background-color: rgb(248, 248, 209);"))
        self.arriveTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.arriveTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.arriveTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.arriveTable.setObjectName(_fromUtf8("arriveTable"))
        self.arriveTable.setColumnCount(0)
        self.arriveTable.setRowCount(0)
        self.arriveTable.horizontalHeader().setStretchLastSection(True)
        self.arriveButtonBar = QtGui.QGroupBox(Dialog)
        self.arriveButtonBar.setGeometry(QtCore.QRect(490, 228, 280, 51))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arriveButtonBar.sizePolicy().hasHeightForWidth())
        self.arriveButtonBar.setSizePolicy(sizePolicy)
        self.arriveButtonBar.setMinimumSize(QtCore.QSize(280, 51))
        self.arriveButtonBar.setMaximumSize(QtCore.QSize(270, 51))
        self.arriveButtonBar.setObjectName(_fromUtf8("arriveButtonBar"))
        self.arriveDeleteButton = QtGui.QPushButton(self.arriveButtonBar)
        self.arriveDeleteButton.setGeometry(QtCore.QRect(188, 18, 80, 23))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete_arrive")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arriveDeleteButton.setIcon(icon3)
        self.arriveDeleteButton.setObjectName(_fromUtf8("arriveDeleteButton"))
        self.arriveAddButton = QtGui.QPushButton(self.arriveButtonBar)
        self.arriveAddButton.setGeometry(QtCore.QRect(16, 18, 80, 23))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/arrive")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arriveAddButton.setIcon(icon4)
        self.arriveAddButton.setObjectName(_fromUtf8("arriveAddButton"))
        self.arriveOpenButton = QtGui.QPushButton(self.arriveButtonBar)
        self.arriveOpenButton.setGeometry(QtCore.QRect(102, 18, 80, 23))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/arrive_edit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.arriveOpenButton.setIcon(icon5)
        self.arriveOpenButton.setObjectName(_fromUtf8("arriveOpenButton"))
        self.fotoArea = QtGui.QGraphicsView(Dialog)
        self.fotoArea.setGeometry(QtCore.QRect(490, 286, 373, 230))
        self.fotoArea.setProperty(_fromUtf8("cursor"), QtCore.Qt.PointingHandCursor)
        self.fotoArea.setMouseTracking(True)
        self.fotoArea.setObjectName(_fromUtf8("fotoArea"))
        self.fotoLabel = QtGui.QLabel(Dialog)
        self.fotoLabel.setGeometry(QtCore.QRect(490, 517, 373, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.fotoLabel.setFont(font)
        self.fotoLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.fotoLabel.setObjectName(_fromUtf8("fotoLabel"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.contract_number, self.last_name)
        Dialog.setTabOrder(self.last_name, self.first_name)
        Dialog.setTabOrder(self.first_name, self.middle_name)
        Dialog.setTabOrder(self.middle_name, self.born_date)
        Dialog.setTabOrder(self.born_date, self.born_place)
        Dialog.setTabOrder(self.born_place, self.passport)
        Dialog.setTabOrder(self.passport, self.passport_given)
        Dialog.setTabOrder(self.passport_given, self.address)
        Dialog.setTabOrder(self.address, self.contact_phone)
        Dialog.setTabOrder(self.contact_phone, self.contact_person)
        Dialog.setTabOrder(self.contact_person, self.addiction_id)
        Dialog.setTabOrder(self.addiction_id, self.addiction_start_date)
        Dialog.setTabOrder(self.addiction_start_date, self.notes)
        Dialog.setTabOrder(self.notes, self.saveButton)
        Dialog.setTabOrder(self.saveButton, self.closeButton)
        Dialog.setTabOrder(self.closeButton, self.arriveAddButton)
        Dialog.setTabOrder(self.arriveAddButton, self.arriveOpenButton)
        Dialog.setTabOrder(self.arriveOpenButton, self.deleteButton)
        Dialog.setTabOrder(self.deleteButton, self.arriveDeleteButton)
        Dialog.setTabOrder(self.arriveDeleteButton, self.female)
        Dialog.setTabOrder(self.female, self.fotoArea)
        Dialog.setTabOrder(self.fotoArea, self.arriveTable)
        Dialog.setTabOrder(self.arriveTable, self.male)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Редактирование записи", None, QtGui.QApplication.UnicodeUTF8))
        self.passpor_group.setTitle(QtGui.QApplication.translate("Dialog", "Паспорт", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Серия, номер", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Выдан", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "Контакт. телефон", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Место рождения", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "Контакт. лицо", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Отчество", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Dialog", "Закрыть", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Дата рождения", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("Dialog", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Адрес прописки", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("Dialog", "Сохранить", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Dialog", "Примечания", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Имя", None, QtGui.QApplication.UnicodeUTF8))
        self.gender.setTitle(QtGui.QApplication.translate("Dialog", "Пол", None, QtGui.QApplication.UnicodeUTF8))
        self.female.setText(QtGui.QApplication.translate("Dialog", "Жен", None, QtGui.QApplication.UnicodeUTF8))
        self.male.setText(QtGui.QApplication.translate("Dialog", "Муж", None, QtGui.QApplication.UnicodeUTF8))
        self.addiction_group.setTitle(QtGui.QApplication.translate("Dialog", "Зависимость", None, QtGui.QApplication.UnicodeUTF8))
        self.addiction_start_date.setDisplayFormat(QtGui.QApplication.translate("Dialog", "yyyy год", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "Началась", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "Тип", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Фамилия", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "№ Договора", None, QtGui.QApplication.UnicodeUTF8))
        self.arriveTable.setSortingEnabled(True)
        self.arriveButtonBar.setTitle(QtGui.QApplication.translate("Dialog", "Прибытие/убытие", None, QtGui.QApplication.UnicodeUTF8))
        self.arriveDeleteButton.setText(QtGui.QApplication.translate("Dialog", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.arriveAddButton.setText(QtGui.QApplication.translate("Dialog", "Добавить", None, QtGui.QApplication.UnicodeUTF8))
        self.arriveOpenButton.setText(QtGui.QApplication.translate("Dialog", "Открыть", None, QtGui.QApplication.UnicodeUTF8))
        self.fotoLabel.setText(QtGui.QApplication.translate("Dialog", "Фотография", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
