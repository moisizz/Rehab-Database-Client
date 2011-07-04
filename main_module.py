# -*- coding: utf8 -*-

'''
Created on 29.06.2011

@author: Моисеев Данил
'''
import sys
import datetime
import VideoCapture
import datetime
from os import remove
from shutil import copyfile
from model import Model

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QString, QDate, QTime

from main_window import Ui_MainWindow as mainWindow
import record_form
import arrive_form
import filter_form

#Три функции для взаимодействия с разлизчными полями Qt формы
def clear_field(field):
    field_type = field.__class__.__name__
    
    if field_type == 'QGroupBox':
        field.children()[0].setChecked(True)
    elif field_type == 'QDateEdit':
        field.setDate(QDate().currentDate())
    elif field_type == 'QComboBox':
        field.setCurrentIndex(0)
    elif field_type == 'QCheckBox':
        field.setChecked(True)
    else:
        field.clear()
        
def set_field_value(field, value):
    field_type = field.__class__.__name__
    
    if field_type == 'QLineEdit':
        field.setText(unicode(value))
        
    elif field_type == 'QGroupBox':
        for choise in field.children():
            if choise.objectName() == value:
                choise.setChecked(True)
                
    elif field_type == 'QDateEdit':
        field.setDate(QDate.fromString(value.encode(), 'dd.MM.yyyy'))
    
    elif field_type == 'QComboBox':
        for i in range(0, field.count()):
            if field.itemData(i) == value:
                field.setCurrentIndex(i)
                break
            
    elif field_type == 'QCheckBox':
        field.setChecked(bool(value))  
        
    elif field_type == 'QPlainTextEdit':
        field.setPlainText(unicode(value))

def get_field_value(field):
    field_type = field.__class__.__name__
    
    if field_type == 'QLineEdit':
        return unicode(field.text())
    elif field_type == 'QGroupBox':
        for choise in field.children():
            if choise.isChecked():
                return unicode(choise.objectName()) 
    elif field_type == 'QDateEdit':
        return unicode(field.date().toString("dd.MM.yyyy"))
    elif field_type == 'QComboBox':
        return field.itemData(field.currentIndex()).toInt()[0]
    elif field_type == 'QPlainTextEdit':
        return unicode(field.toPlainText())
    elif  field_type == 'QCheckBox':
        return int(field.isChecked())


class Application(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.setLayout(self.ui.mainLayout)
        
        self.recordDialog = recordDialog(self)
        self.filterDialog = filterDialog(self)
        
        self.connect(self.ui.mainTable,        SIGNAL('cellDoubleClicked(int, int)'), self.open_record_slot)
        self.connect(self.ui.createBaseAction, SIGNAL('triggered()'),                 self.create_base_slot)
        self.connect(self.ui.openBaseAction,   SIGNAL('triggered()'),                 self.open_base_slot)
        self.connect(self.ui.openButton,       SIGNAL('clicked()'),                   self.open_record_slot)
        self.connect(self.ui.addButton,        SIGNAL('clicked()'),                   self.recordDialog.open_empty_record)
        self.connect(self.ui.deleteButton,     SIGNAL('clicked()'),                   self.delete_record_slot)
        self.connect(self.ui.filterButton,     SIGNAL('clicked()'),                   self.open_filter_slot)

        #-------------Временное----------------
        """self.enable_buttons()
        self.db = Model({'database_path':'database.db'})
        self.addictions = self.db.get_addictions()
        self.fill_person_table()"""
        #--------------------------------------
   
    def execute(self):
        """Исполнение приложения"""
        self.show()
        sys.exit(self.app.exec_())
   
    def open_base_slot(self):
        """Реакция на нажание 'Открыть базу' в главном меню"""
        path = str(QtGui.QFileDialog.getOpenFileName(self, u"Открыть базу", u"", u"Базы данных (*.db)"))

        if path != '':
            if hasattr(self, 'db'):
                self.db.close_connection()
                
            self.db = Model({'database_path':path})
            
            self.enable_buttons()
            self.addictions = self.db.get_addictions()
            self.fill_person_table()
   
    def create_base_slot(self):
        """Реакция на нажание 'Создать пустую базу' в главном меню"""
        path = str(QtGui.QFileDialog.getSaveFileName(self, u"Создать новую базу", u"", u"Базы данных (*.db)"))

        if path != '':
            if hasattr(self, 'db'):
                self.db.close_connection()
                
            self.db = Model({'database_path':path})
            self.db.create_empty_tables()
            
            self.enable_buttons()
            self.addictions = self.db.get_addictions()

    def open_record_slot(self):
        """Реакция на нажатие кнопки Открыть"""
        
        selected_row_num = self.ui.mainTable.currentRow()
        
        if selected_row_num != -1:
            selected_record_id = int(self.ui.mainTable.item(selected_row_num, 0).text())
            record = self.db.get_person(selected_record_id)
            
            self.recordDialog.open_record(record)
        
    def delete_record_slot(self):
        selected_record_num = self.ui.mainTable.currentRow()
        
        if selected_record_num != -1:
            record_id = self.person_list[selected_record_num][0]
        
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

            if confirm == QtGui.QMessageBox.Ok:
                self.db.delete_record('person', record_id)
                self.fill_person_table() # --------здесь нужно будет изменить

    def fill_person_table(self):
        """Заполнение таблицы людей"""
        person_schema = self.db.person_schema
        person_table = self.ui.mainTable
        
        #Задаем количество колонок таблицы
        person_table.setColumnCount(len(person_schema))

        #Создаем шапку таблицы        
        for i in range(0, len(person_schema)):
            if person_schema[i]['title'] != '':
                header_item = QtGui.QTableWidgetItem(unicode(person_schema[i]['title']))
                person_table.setHorizontalHeaderItem(i, header_item)
        
        #Получаем список людей из базы
        person_list = self.db.get_person_list()
        self.person_list = person_list
        
        #Задаем число строк
        person_table.setRowCount(len(person_list))
        
        #Заполняем таблицу
        for i in range(0, len(person_list)):
            for j in range(0, len(person_schema)):
                #Если колонка пола
                if(person_schema[j]['col_name'] == 'gender'):
                    if(person_list[i][j] == 'male'):
                        value = u'муж.'
                    else:
                        value = u'жен.'
                        
                elif (person_schema[j]['col_name'] == 'addiction_type'):
                    for row in self.addictions:
                        if person_list[i][j] == row[0]:
                            value = row[1]
                    
                else:
                    value = unicode(person_list[i][j])
                
                item = QtGui.QTableWidgetItem(value)
                person_table.setItem(i, j, item)

    def open_filter_slot(self):
        self.filterDialog.show()

    def enable_buttons(self):
        self.ui.addButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)
        self.ui.openButton.setEnabled(True)
        self.ui.filterButton.setEnabled(True)
        
                
class recordDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = record_form.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.arriveDialog = arriveDialog(self)
        
        self.connect(self.ui.closeButton, SIGNAL('clicked()'), self.close_button_slot)
        self.connect(self.ui.saveButton, SIGNAL('clicked()'), self.save_record_slot)
        self.connect(self.ui.deleteButton, SIGNAL('clicked()'), self.delete_record_slot)
        self.connect(self.ui.middle_name, SIGNAL('editingFinished()'), self.detect_gender_slot)
        self.connect(self.ui.last_name, SIGNAL('textEdited(QString)'), self.jump_from_last_name_field)
        self.connect(self.ui.first_name, SIGNAL('textEdited(QString)'), self.jump_from_first_name_field)
        self.connect(self.ui.middle_name, SIGNAL('textEdited(QString)'), self.jump_from_middle_name_field)
        self.connect(self.ui.arriveTable, SIGNAL('itemSelectionChanged()'), self.change_arrive_foto)
        self.connect(self.ui.arriveOpenButton, SIGNAL('clicked()'), self.open_arrive_record_slot)
        self.connect(self.ui.arriveAddButton, SIGNAL('clicked()'), self.open_empty_arrive_slot)
        self.connect(self.ui.arriveDeleteButton, SIGNAL('clicked()'), self.delete_arrive_record_slot)
        self.connect(self.ui.arriveTable,        SIGNAL('cellDoubleClicked(int, int)'), self.open_arrive_record_slot)

    def fill_addiction_list(self):
        addiction_list = self.db.get_addictions()
        
        self.ui.addiction_type.clear()
        
        for addiction in addiction_list:
            self.ui.addiction_type.addItem(addiction[1], addiction[0])

    def clear_fields(self):
        self.db = self.parent().db
        schema = self.db.person_schema
        
        for row in schema:
            if hasattr(self.ui, row['col_name']):
                field = getattr(self.ui, row['col_name'])
                clear_field(field)
                
        self.ui.male.setChecked(True)
        self.ui.arriveTable.setRowCount(0)
        self.ui.arriveTable.setColumnCount(0)
        self.ui.arriveTable.clear()
        
        scene = QtGui.QGraphicsScene()
        self.ui.fotoArea.setScene(scene) 
 
    def disable_empty_part(self):
        self.ui.arriveTable.setEnabled(False)
        self.ui.fotoBox.setEnabled(False)
        self.ui.arriveAddButton.setEnabled(False)
        self.ui.arriveDeleteButton.setEnabled(False)
        self.ui.arriveOpenButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
    
    def enable_empty_part(self):
        self.ui.arriveTable.setEnabled(True)
        self.ui.fotoBox.setEnabled(True)
        self.ui.arriveAddButton.setEnabled(True)
        self.ui.arriveDeleteButton.setEnabled(True)
        self.ui.arriveOpenButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)
 
    def open_record(self, record):
        """Открытие формы и заполнение ее значениями"""
        self.clear_fields()
        self.db = self.parent().db
        self.ui.saveButton.setText(u'Сохранить')
 
        self.record = record
        schema = self.db.person_schema
        self.enable_empty_part()
        self.fill_addiction_list()
        
        for i in range(0, len(record)):
            record_field_value = record[i]
            col_name = schema[i]['col_name']
            
            if hasattr(self.ui, col_name):
                field = getattr(self.ui, col_name)
                set_field_value(field, record_field_value)

        self.fill_person_arrive_table()

        self.state = 'open_record'  
        self.show()

    def open_empty_record(self):
        self.clear_fields()
        self.ui.saveButton.setText(u'Добавить')
        self.disable_empty_part()
        self.fill_addiction_list()
        
        self.state = 'create_record'
        self.show()

    def get_record_values(self):
        record_values = {}
        schema = self.db.person_schema
        
        for i in range(0, len(schema)):
            if hasattr(self.ui, schema[i]['col_name']):
                field = getattr(self.ui, schema[i]['col_name'])
                field_value = get_field_value(field)
                record_values[schema[i]['col_name']] = field_value
                
        return record_values
            
    def save_record_slot(self): 
        new_record_values = self.get_record_values()
        
        is_record_changed = False
        
        if self.state == 'open_record':
            updated_values = {}
            schema = self.db.person_schema
            
            for i in range(0, len(schema)):
                col_name = schema[i]['col_name']
                
                if hasattr(self.ui, col_name):
                    old_value = self.record[i]
                    new_value = new_record_values[col_name]
                    
                    if old_value != new_value:
                        updated_values[col_name] = new_value
                        is_record_changed = True
                        
            if is_record_changed:
                self.record = self.db.update_record('person', self.record[0], updated_values)
                self.parent().fill_person_table() #--- скорее всего здесь нужно что-то другое
        
        elif self.state == 'create_record':
            #Запоминаем текущую дату для поля дата контракта
            new_record_values['contract_date'] = str(QDate().currentDate().toString("dd.MM.yyyy"))
                
            self.record = self.db.insert_record('person', new_record_values)
            
            self.fill_person_arrive_table()
            
            self.state = 'open_record'            
            self.enable_empty_part()
            self.ui.saveButton.setText(u'Сохранить')
            self.parent().fill_person_table() #--- скорее всего здесь поонадобится что-то другое

    def delete_record_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
            u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
            QtGui.QMessageBox.Ok | 
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        if confirm == QtGui.QMessageBox.Ok:
            self.db.delete_record('person', self.record[0])
            
            self.parent().fill_person_table() #------------ здесь будет что-то другое
            
            self.hide()

    def fill_person_arrive_table(self):
        self.arrive_list = self.db.get_arrive_list(self.record[0])
        arrive_list = self.arrive_list
        schema = self.db.arrive_schema
        
        arrive_table = self.ui.arriveTable
            
        displayed_columns_count = 0
        
        for i in range(0, len(schema)):
            if schema[i]['title'] != '':
                displayed_columns_count += 1
        
        arrive_table.setColumnCount(displayed_columns_count)

        current_column_num = 0

        for i in range(0, len(schema)):
            if schema[i]['title'] != '':
                header_item = QtGui.QTableWidgetItem(QString(schema[i]['title']))
                arrive_table.setHorizontalHeaderItem(current_column_num, header_item)
                current_column_num += 1
                
        if len(arrive_list) != 0:
                
            arrive_table.setRowCount(len(arrive_list))
            
            for i in range(0, len(arrive_list)):
                current_column_num = 0
                for j in range(0, len(schema)):
                    if schema[j]['title'] != '':
                        if (schema[j]['col_name'] == 'is_cure') and (arrive_list[i][j] == 1):
                            value = u'Да'
                        elif (schema[j]['col_name'] == 'is_cure') and (arrive_list[i][j] == 0):
                            value = u'Нет'
                        else:
                            value = unicode(arrive_list[i][j])
                        item = QtGui.QTableWidgetItem(value)
                        arrive_table.setItem(i, current_column_num, item)
                        current_column_num += 1
            
            scene = QtGui.QGraphicsScene()
            if arrive_list[0][-1] != '':
                pixmap = QtGui.QPixmap("images/%s" % arrive_list[0][-1]). \
                                                       scaledToHeight(self.ui.fotoArea.height()/2, 1). \
                                                       scaledToWidth(self.ui.fotoArea.width()/2, 1)
                scene.addPixmap(pixmap)
            self.ui.fotoArea.setScene(scene)  

    def detect_gender_slot(self):
        rd = self.ui
        
        middle_name = rd.middle_name.text()
        
        ending = middle_name.section('',len(middle_name)-2,len(middle_name))
        
        if ending == u'вна':
            pass
            rd.female.setChecked(True)
        elif ending == u'вич':
            rd.male.setChecked(True)
        
    def jump_from_last_name_field(self, str):
        if str != '' and str[len(str)-1] == ' ':
            self.ui.last_name.setText(str[0:-1])
            self.ui.first_name.setFocus()
        
    def jump_from_first_name_field(self, str):
        if str != '' and str[len(str)-1] == ' ':
            self.ui.first_name.setText(str[0:-1])
            self.ui.middle_name.setFocus()
            
    def jump_from_middle_name_field(self, str):
        if str != '' and str[len(str)-1] == ' ':
            self.ui.middle_name.setText(str[0:-1])
            self.ui.born_date.setFocus()
        
    def change_arrive_foto(self):
        selected_record_id = self.ui.arriveTable.currentRow()
        
        scene = QtGui.QGraphicsScene()
        if self.arrive_list[selected_record_id][-1] != '':
            pixmap = QtGui.QPixmap("images/%s" % self.arrive_list[selected_record_id][-1]). \
                                                   scaledToHeight(self.ui.fotoArea.height()/1.4, 1). \
                                                   scaledToWidth(self.ui.fotoArea.width()/1.4, 1)
            scene.addPixmap(pixmap)
        self.ui.fotoArea.setScene(scene)  
        
    def open_arrive_record_slot(self):
        selected_record_num = self.ui.arriveTable.currentRow()
        record = self.arrive_list[selected_record_num]
        
        self.arriveDialog.db = self.db
        self.arriveDialog.open_arrive_record(record)
        
    def open_empty_arrive_slot(self):
        self.arriveDialog.db = self.db
        self.arriveDialog.open_empty_record()
 
    def delete_arrive_record_slot(self):
        selected_record_num = self.ui.arriveTable.currentRow()
        
        if selected_record_num != -1:
            record_id = self.arrive_list[selected_record_num][0]
        
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

            if confirm == QtGui.QMessageBox.Ok:
                self.db.delete_record('arrive', record_id)
                self.fill_person_arrive_table() # --------здесь нужно будет изменить
 
    def close_button_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение закрытия',
            u"Вы уверены, что хотите закрыть форму?\nВсе введенные вами данные будут потеряны!", 
            QtGui.QMessageBox.Ok | 
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        if confirm == QtGui.QMessageBox.Ok:
            self.hide()
        
        
class arriveDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = arrive_form.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.connect(self.ui.makeFoto, SIGNAL('clicked()'), self.make_foto_slot)
        self.connect(self.ui.openFoto, SIGNAL('clicked()'), self.open_foto_slot)
        self.connect(self.ui.saveButton, SIGNAL('clicked()'), self.save_record_slot)
        self.connect(self.ui.deleteButton, SIGNAL('clicked()'), self.delete_record_slot)
        self.connect(self.ui.closeButton, SIGNAL('clicked()'), self.close_slot)

    def clear_fields(self):
        self.db = self.parent().db
        schema = self.db.arrive_schema
        
        for row in schema:
            if hasattr(self.ui, row['col_name']):
                field = getattr(self.ui, row['col_name'])
                clear_field(field)
                
        scene = QtGui.QGraphicsScene()
        self.ui.fotoArea.setScene(scene)  
        
        if hasattr(self, 'fotoname'):
            del(self.fotoname)
    
    def get_record_values(self):
        schema = self.db.arrive_schema
        
        values = {}
        
        for i in range(0, len(schema)):
            if hasattr(self.ui, schema[i]['col_name']):
                field = getattr(self.ui, schema[i]['col_name'])
                value = get_field_value(field)
                values[schema[i]['col_name']] = value
    
            if schema[i]['col_name'] == 'foto':
                if hasattr(self, 'fotoname'):
                    values['foto'] = str(self.fotoname)
        
        return values 
    
    def open_arrive_record(self, record):
        self.record = record
        self.clear_fields()
        
        schema = self.db.arrive_schema
        
        for i in range(0, len(schema)):
            if(hasattr(self.ui, schema[i]['col_name'])):
                field = getattr(self.ui, schema[i]['col_name'])
                set_field_value(field, record[i])
                
            if(schema[i]['col_name'] == 'foto'):
                self.fotoname = record[i]
                scene = QtGui.QGraphicsScene()
                scene.addPixmap(QtGui.QPixmap("images/%s" % self.fotoname))
                self.ui.fotoArea.setScene(scene) 
        
        self.state = 'open_record'
        self.show()
    
    def open_empty_record(self):
        self.clear_fields()
        self.ui.deleteButton.setEnabled(False)
        self.ui.saveButton.setText(u'Добавить')
        self.state = 'create_record'
        self.show()
    
    def make_foto_slot(self):
        confirmation = True
        
        if hasattr(self, 'fotoname'):
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение изменения фотографии',
                u"Вы уверены, что хотите снять новую фотографию?\nСтарая будет удалена после сохранения", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
    
            if confirm == QtGui.QMessageBox.Cancel:
                confirmation = False
        
        if confirmation:
            camera = VideoCapture.Device()
            self.fotoname = QDate().currentDate().toString('dd.MM.yyyy') + '_' + \
                            QTime().currentTime().toString('HH-mm-ss-zz') + '.png'
                       
                    
            camera.saveSnapshot('images/%s' %  self.fotoname, timestamp=True)
            
            scene = QtGui.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap("images/%s" % self.fotoname))
            self.ui.fotoArea.setScene(scene)   
   
    def open_foto_slot(self):
        path = str(QtGui.QFileDialog.getOpenFileName(self, u"Открыть фото", u""))
    
        if path != '':
            self.fotoname = QDate().currentDate().toString('dd.MM.yyyy') + '_' + \
                            QTime().currentTime().toString('HH-mm-ss-zz') + '.png'
                       
            copyfile(path, 'images/%s' % self.fotoname)
     
            ar = self.ui
            img = '<img width="%s" src="images/%s">' % (self.ui.fotoArea.width(),  self.fotoname)
            ar.fotoArea.setText(img)
        
    def save_record_slot(self):
        new_record_values = self.get_record_values()
        schema = self.db.arrive_schema
        
        if self.state == 'open_record':
            new_record_values['id'] = self.record[0]
            new_record_values['person_id'] = self.record[1]
            updated_values = {}
            is_changed = False
            for i in range(0, len(schema)):
                col_name = schema[i]['col_name']
                
                old_value = self.record[i]
                new_value = new_record_values[col_name]
                
                if old_value != new_value:
                    updated_values[col_name] = new_value
                    is_changed = True
        
            if is_changed:
                if hasattr(new_record_values, 'foto'):
                    for i in range(0, len(schema)):
                        if schema[i]['col_name'] == 'foto':
                            old_foto = self.record[i]
                            remove('images/%s' % old_foto)
                            
                self.record = self.db.update_record('arrive', new_record_values['id'], new_record_values)
                self.parent().fill_person_arrive_table()
        
        if self.state == 'create_record':
            new_record_values['person_id'] = self.parent().record[0]
            self.record = self.db.insert_record('arrive', new_record_values)
            
            self.ui.saveButton.setText(u'Сохнатить')
            self.ui.deleteButton.setEnabled(True)
            self.parent().fill_person_arrive_table()
            self.state = 'open_record'
     
    def delete_record_slot(self):
        record_id = self.record[0]
    
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
            u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
            QtGui.QMessageBox.Ok | 
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        if confirm == QtGui.QMessageBox.Ok:
            self.db.delete_record('arrive', record_id)
            self.parent().fill_person_arrive_table() # --------здесь нужно будет изменить
            self.hide()
        
    def close_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение закрытия формы',
                u"Вы уверены что хотите закрыть форму?\nВсе введенные данные будут потеряны", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
    
        if confirm == QtGui.QMessageBox.Ok:
            self.hide()
    
     
class filterDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = filter_form.Ui_Dialog()
        self.ui.setupUi(self)

if __name__ == '__main__':    
    app = Application()
    app.execute()