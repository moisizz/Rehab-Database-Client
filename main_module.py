# -*- coding: utf8 -*-

import sys
import VideoCapture
from os import remove, getcwdu, mkdir
from os.path import join, isdir, isfile
from model import Model, Person, Arrive, Addiction, SendAddress
from sqlalchemy.orm.query import Query
from PIL import Image
import yaml

from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, QDate, QTime, pyqtSignal, Qt

from main_window import Ui_MainWindow as mainWindow
import record_form
import arrive_form
import filter_form
import catalogs_form

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
        field.setChecked(False)
    else:
        field.clear()
        
def set_field_value(field, value):
    field_type = field.__class__.__name__
    
    if field_type == 'QLineEdit':
        field.setText(unicode(value))
        
    elif field_type == 'QGroupBox':
        for choise in field.children():
            if (choise.objectName() == 'male') and (value == Person.male):
                choise.setChecked(True)
            elif (choise.objectName() == 'female') and (value == Person.female):
                choise.setChecked(True)
                
    elif field_type == 'QDateEdit':
        field.setDate(QDate(value))
    
    elif field_type == 'QComboBox':
        if field.objectName() == 'leave_cause_id':
            for i in range(0, field.count()):
                if field.itemData(i).toList()[0].toInt()[0] == value:
                    field.setCurrentIndex(i)
                    break
        else:
            for i in range(0, field.count()):
                if field.itemData(i).toInt()[0] == value:
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
            if choise.isChecked() and choise.objectName() == 'male':
                return Person.male
            elif choise.isChecked() and choise.objectName() == 'female':
                return Person.female
    elif field_type == 'QDateEdit':
        return field.date().toPyDate()
    elif field_type == 'QComboBox':
        if field.objectName() == 'leave_cause_id':
            value = field.itemData(field.currentIndex()).toList()[0].toInt()[0]
        else:
            value = field.itemData(field.currentIndex()).toInt()[0]
        if value == -1:
            return None
        else:
            return value 
    elif field_type == 'QPlainTextEdit':
        return unicode(field.toPlainText())
    elif  field_type == 'QCheckBox':
        return int(field.isChecked())


class Application(QtGui.QMainWindow):
    databaseOpenSignal = pyqtSignal(Model)
    
    def __init__(self, parent=None):
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.setLayout(self.ui.mainLayout)
        self.ui.buttonBox.setLayout(self.ui.buttonBoxLayout)

        self.ui.recordCount = QtGui.QLabel(u'') 
        self.ui.statusbar.addPermanentWidget(self.ui.recordCount)

        if not isfile('config.yaml'):
            self.generate_new_configuration()
        else:
            self.config = yaml.load(file('config.yaml', 'r'))

        #Список отображаемых колонок и их заголовков
        self.displayed_person_columns = (
         [{'name':'id','title':u'№ договора'},
          {'name':'contract_date','title':u'Дата договора'},
          {'name':'last_name','title':u'Фамилия'},
          {'name':'first_name','title':u'Имя'},
          {'name':'middle_name','title':u'Отчество'},
          {'name':'gender','title':u'Пол'},
          {'name':'born_date','title':u'Дата рождения'},
          {'name':'born_place','title':u'Место рождения'},
          {'name':'passport_series','title':u'Серия паспорта'},
          {'name':'passport_number','title':u'№ Паспорта'},
          {'name':'passport_given','title':u'Паспорт выдан'},
          {'name':'address','title':u'Адрес прописки'},
          {'name':'contact_phone','title':u'Контакт. телефон'},
          {'name':'contact_person','title':u'Контакт. лицо'},
          {'name':'addiction_id','title':u'Зависимость'},
          {'name':'addiction_start_date','title':u'Длительность (лет)'},
          {'name':'notes','title':u'Примечания'}])
        
        self.recordDialog = recordDialog(self)
        self.filterDialog = filterDialog(self)
        self.catalogsDialog = catalogsDialog(self)
        
        self.databaseOpenSignal.connect(self.recordDialog.database_opened_slot)
        self.databaseOpenSignal.connect(self.recordDialog.arriveDialog.database_opened_slot)
        self.databaseOpenSignal.connect(self.filterDialog.database_opened_slot)
        self.databaseOpenSignal.connect(self.catalogsDialog.database_opened_slot)
        
        self.recordDialog.tableUpdated.connect(self.update_table_slot)
        self.filterDialog.tableFiltered.connect(self.fill_person_table)
        
        self.catalogsDialog.addictionsChanged.connect(self.recordDialog.fill_addiction_list)
        self.catalogsDialog.addictionsChanged.connect(self.filterDialog.fill_addiction_list)
        self.catalogsDialog.addressesChanged.connect(self.recordDialog.arriveDialog.fill_send_address_list)
        
        self.connect(self.ui.refreshButton,       SIGNAL('clicked()'),                    self.fill_person_table)
        self.connect(self.ui.mainTable,            SIGNAL('cellDoubleClicked(int, int)'), self.open_record_slot)
        self.connect(self.ui.createBaseAction,     SIGNAL('triggered()'),                 self.create_base_slot)
        self.connect(self.ui.openBaseAction,       SIGNAL('triggered()'),                 self.open_base_slot)
        self.connect(self.ui.imagesPathEditAction, SIGNAL('triggered()'),                 self.edit_images_path)
        self.connect(self.ui.catalogEditAction,    SIGNAL('triggered()'),                 self.catalogsDialog.show)
        self.connect(self.ui.openButton,           SIGNAL('clicked()'),                   self.open_record_slot)
        self.connect(self.ui.addButton,            SIGNAL('clicked()'),                   self.recordDialog.open_empty_record)
        self.connect(self.ui.deleteButton,         SIGNAL('clicked()'),                   self.delete_record_slot)
        self.connect(self.ui.filterButton,         SIGNAL('clicked()'),                   self.open_filter_slot)

        if self.config['paths'].has_key('database') and isfile(self.config['paths']['database']):
            self.open_base(self.config['paths']['database'])
   
    def generate_new_configuration(self):
        img_path = join(getcwdu(),'images')
        self.config = {'paths': {'images': img_path}}

        self.update_configuration()
        
    def update_configuration(self):
        f = file('config.yaml', 'w')
        
        if not isfile('config.yaml'):
            f.write('')
        
        yaml.dump(self.config, f)
        
        f.close()
     
    def edit_images_path(self):        
        path = unicode(QtGui.QFileDialog.getExistingDirectory(self, u"Изменить директорию фотографий", self.config['paths']['images']))

        if path != '':
            self.config['paths']['images'] = path
            self.update_configuration()
        
    def execute(self):
        """Исполнение приложения"""
        self.show()
        sys.exit(self.app.exec_())
   
    def close_database(self):
        self.db.close_connection()
        self.ui.mainTable.clear()
        self.ui.mainTable.setRowCount(0)
        self.ui.mainTable.setColumnCount(0)
        self.ui.catalogEditAction.setEnabled(False)
    
    def open_base(self, path):
        if hasattr(self, 'db'):
            self.close_database()
            
        try:
            self.db = Model({'database_path':path})
        except IOError:
            sys.exit(IOError.message)
            
        self.databaseOpenSignal.emit(self.db)
        
        self.enable_buttons()
        self.fill_person_table()
       
    def open_base_slot(self):
        """Реакция на нажание 'Открыть базу' в главном меню"""
        path = unicode(QtGui.QFileDialog.getOpenFileName(self, u"Открыть базу", unicode(getcwdu()), u"Базы данных (*.db)"))

        if path != '':
            self.open_base(path)
            
            self.config['paths']['database'] = path
            self.update_configuration()
   
    def create_base_slot(self):
        """Реакция на нажание 'Создать пустую базу' в главном меню"""
        path = unicode(QtGui.QFileDialog.getSaveFileName(self, u"Создать новую базу", unicode(getcwdu()), u"Базы данных (*.db)"))

        if path != '':
            if hasattr(self, 'db'):
                self.close_database()
                
            try:    
                self.db = Model({'database_path':path})
            except IOError:
                sys.exit(IOError.message)
            
            self.config['paths']['database'] = path
            self.update_configuration()
                
            self.db.create_empty_tables()
            
            self.enable_buttons()
            self.fill_person_table()
            self.addictions = self.db.get_addictions()
            
            self.databaseOpenSignal.emit(self.db)

    def open_record_slot(self, row=None, col=None):
        """Реакция на нажатие кнопки Открыть"""
        if (row == None) and (col == None):
            row = self.ui.mainTable.currentRow()
            col = self.ui.mainTable.currentColumn()
        
        table = self.ui.mainTable
        
        if table.currentRow() != -1:
            table_item = table.item(row, 0)
            record = table_item.record
            
            self.recordDialog.open_record(record)
        
    def delete_record_slot(self):
        selected_record_num = self.ui.mainTable.currentRow()
        
        if selected_record_num != -1:
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

            if confirm == QtGui.QMessageBox.Ok:
                record = self.ui.mainTable.item(selected_record_num, 0).record
                
                try:
                    self.db.delete_record(record)
                except IOError:
                    sys.exit(IOError)
                    
                self.update_table_slot(record, 'delete')

    def update_table_slot(self, record, record_update_type):
        table = self.ui.mainTable
        
        if record_update_type == 'create':
            table.setRowCount(table.rowCount()+1)
            columns = self.displayed_person_columns
            
            new_record_index = table.rowCount()-1
            
            for j in range(0, len(columns)):
                self.fill_cell(new_record_index, j, columns[j]['name'], record)
                
        else:
            for i in range(0, table.rowCount()):
                table_record = table.item(i, 0).record
                
                if record.id == table_record.id:
                    if record_update_type == 'update':
                        columns = self.displayed_person_columns
                        
                        for j in range(0, len(columns)):
                            self.fill_cell(i, j, columns[j]['name'], record)
                        
                    elif record_update_type == 'delete':
                        table.removeRow(i)
                    
                    break
                
        self.ui.recordCount.setText(u'Количество записей = %s' % self.ui.mainTable.rowCount())
    
    def fill_person_table(self, query=None):
        """Заполнение таблицы людей"""
        if query == None:
            person_list = self.db.get_person_list()
        else:
            person_list = query.all()
        
        record_count = len(person_list)
        
        self.ui.recordCount.setText(u'Количество записей = %s' % record_count)
        
        columns = self.displayed_person_columns

        #Задаем количество колонок таблицы
        table = self.ui.mainTable
        table.clear()
        table.setColumnCount(len(columns))

        #Создаем шапку таблицы        
        for i in range(0, len(columns)):
            col_title = columns[i]['title']
            header_item = QtGui.QTableWidgetItem(col_title)
            header_item.setFont(QtGui.QFont("Trebuchet MS", pointSize=8))
            table.setHorizontalHeaderItem(i, header_item)

        #Задаем число строк
        table.setRowCount(len(person_list))
        table.records =[]
        
        #Заполняем таблицу
        for i in range(0, len(person_list)):
            for j in range(0, len(columns)):
                self.fill_cell(i, j, columns[j]['name'], person_list[i])
              
    def fill_cell(self, row, col, column_name, record):

        #Если колонка пола
        if(column_name == 'gender'):
            if(getattr(record, column_name) == Person.male):
                value = u'Муж.'
            else:
                value = u'Жен.'
                
        elif (column_name == 'addiction_id'):
            value = record.addiction.name
            
        elif (column_name == 'addiction_start_date'):
            start_date = QDate(getattr(record, column_name)).year()
            current_date = QDate().currentDate().year()
            
            dlit = current_date - start_date
            value = unicode(dlit)
            
        elif (column_name == 'contract_date') or (column_name == 'born_date'):
            value = QDate(getattr(record, column_name)).toString('dd.MM.yyyy')
            
        else:
            value = unicode(getattr(record, column_name))
        
        item = QtGui.QTableWidgetItem(value)
        
        #Сохраняем запись в объекте первой ячейки ряда
        if col == 0:
            item.record = record
            
        self.ui.mainTable.setItem(row, col, item)
                
    def open_filter_slot(self):
        self.filterDialog.show()

    def enable_buttons(self):
        self.ui.refreshButton.setEnabled(True)
        self.ui.addButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)
        self.ui.openButton.setEnabled(True)
        self.ui.filterButton.setEnabled(True)
        self.ui.catalogEditAction.setEnabled(True)
        
                
class recordDialog(QtGui.QDialog):
    tableUpdated = pyqtSignal(Person, str)
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = record_form.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowFlags(Qt.Window)
        
        self.ui.mainLayout = QtGui.QHBoxLayout(self)
        
        self.ui.rightSideLayout = QtGui.QVBoxLayout()
        self.ui.rightSideLayout.addWidget(self.ui.fotoLabel)
        self.ui.rightSideLayout.addWidget(self.ui.fotoArea)
        self.ui.rightSideLayout.addWidget(self.ui.arriveTable)
        self.ui.rightSideLayout.addWidget(self.ui.arriveButtonBar) 
        
        self.ui.mainLayout.addWidget(self.ui.mainBox)
        self.ui.mainLayout.addLayout(self.ui.rightSideLayout)
        
        
        
        self.config = self.parent().config
        
        self.displayed_arrive_columns = (
        [{'name': 'arrive_date', 'title': u'Прибыл'},
         {'name': 'leave_date', 'title': u'Убыл'},
         {'name': 'leave_cause', 'title': u'Причина'},
         {'name': 'is_cure', 'title': u'Долечился'},
         {'name': 'send_address_id', 'title': u'Адрес отправки'}])
        
        self.arriveDialog = arriveDialog(self)
        self.arriveDialog.tableUpdated.connect(self.update_table_slot)
        
        self.connect(self.ui.closeButton, SIGNAL('clicked()'), self.close_button_slot)
        self.connect(self.ui.saveButton, SIGNAL('clicked()'), self.save_record_slot)
        self.connect(self.ui.deleteButton, SIGNAL('clicked()'), self.delete_record_slot)
        self.connect(self.ui.middle_name, SIGNAL('editingFinished()'), self.detect_gender_slot)
        self.connect(self.ui.last_name, SIGNAL('textEdited(QString)'), self.jump_from_last_name_field)
        self.connect(self.ui.first_name, SIGNAL('textEdited(QString)'), self.jump_from_first_name_field)
        self.connect(self.ui.middle_name, SIGNAL('textEdited(QString)'), self.jump_from_middle_name_field)
        self.connect(self.ui.arriveTable, SIGNAL('cellClicked(int, int)'), self.change_arrive_foto)
        self.connect(self.ui.arriveOpenButton, SIGNAL('clicked()'), self.open_arrive_record_slot)
        self.connect(self.ui.arriveAddButton, SIGNAL('clicked()'), self.open_empty_arrive_slot)
        self.connect(self.ui.arriveDeleteButton, SIGNAL('clicked()'), self.delete_arrive_record_slot)
        self.connect(self.ui.arriveTable,        SIGNAL('cellDoubleClicked(int, int)'), self.open_arrive_record_slot)

    def database_opened_slot(self, database):
        self.close()
        self.db = database
        self.fill_addiction_list()

    def clear_fields(self):
        self.arriveDialog.close()
        for row in self.record.get_columns_names():
            if hasattr(self.ui, row):
                field = getattr(self.ui, row)
                clear_field(field)
                
        self.ui.male.setChecked(True)
        self.ui.arriveTable.setRowCount(0)
        self.ui.arriveTable.setColumnCount(0)
        self.ui.arriveTable.clear()
        
        scene = QtGui.QGraphicsScene()
        self.ui.fotoArea.setScene(scene) 
            
    def fill_addiction_list(self):
        addiction_list = self.db.get_addictions()
        
        addiction_list_widget = self.ui.addiction_id
        addiction_list_widget.clear()
        
        for i in range(0, len(addiction_list)):
            addiction_list_widget.addItem(addiction_list[i].name, addiction_list[i].id)
 
    def disable_empty_part(self):
        self.ui.arriveTable.setEnabled(False)
        self.ui.fotoArea.setEnabled(False)
        self.ui.arriveAddButton.setEnabled(False)
        self.ui.arriveDeleteButton.setEnabled(False)
        self.ui.arriveOpenButton.setEnabled(False)
        self.ui.deleteButton.setEnabled(False)
    
    def enable_empty_part(self):
        self.ui.arriveTable.setEnabled(True)
        self.ui.fotoArea.setEnabled(True)
        self.ui.arriveAddButton.setEnabled(True)
        self.ui.arriveDeleteButton.setEnabled(True)
        self.ui.arriveOpenButton.setEnabled(True)
        self.ui.deleteButton.setEnabled(True)
 
    def open_record(self, record):
        """Открытие формы и заполнение ее значениями"""
        self.record = record

        self.clear_fields()
        self.ui.saveButton.setText(u'Сохранить')
 
        self.enable_empty_part()
        
        columns = record.get_columns_names()
        
        for column in columns:
            record_field_value = getattr(record, column)
            
            if hasattr(self.ui, column):
                field = getattr(self.ui, column)
                set_field_value(field, record_field_value)

        self.fill_person_arrive_table()

        self.state = 'open_record'  
        self.show()

    def open_empty_record(self):
        self.record = Person({})
        self.clear_fields()
        self.ui.saveButton.setText(u'Добавить')
        self.disable_empty_part()
        
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
        if self.state == 'open_record':
            is_record_changed = False

            record = self.record
            columns = record.get_columns_names()
            
            for i in range(0, len(columns)):
                col_name = columns[i]
                
                if hasattr(self.ui, col_name):
                    old_value = getattr(self.record, col_name)
                    new_value = get_field_value(getattr(self.ui, col_name))
                    
                    if old_value != new_value:
                        is_record_changed = True
                        setattr(record, col_name, new_value)
                        
            if is_record_changed:
                self.db.update_records()
                self.tableUpdated.emit(record, 'update')
        
        elif self.state == 'create_record':
            new_record = self.record
            values = {}
            
            #Запоминаем текущую дату для поля дата контракта
            columns = self.record.get_columns_names()
            for column_name in columns:
                if hasattr(self.ui, column_name):
                    field = getattr(self.ui, column_name)
                    values[column_name] = get_field_value(field)
                
            new_record.set_values(values)
                
            try:
                self.db.insert_record(new_record)
            except IOError:
                sys.exit(IOError)
                
            self.record = new_record
            self.tableUpdated.emit(new_record, 'create')
            
            self.fill_person_arrive_table()
            self.state = 'open_record'            
            self.enable_empty_part()
            self.ui.saveButton.setText(u'Сохранить')

    def delete_record_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
            u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
            QtGui.QMessageBox.Ok | 
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        if confirm == QtGui.QMessageBox.Ok:
            try:
                self.db.delete_record(self.record)
            except IOError:
                sys.exit(IOError)
                
            self.tableUpdated.emit(self.record, 'delete')
            self.hide()

    def fill_person_arrive_table(self):
        arrive_list = self.record.arrives
        table = self.ui.arriveTable
        columns = self.displayed_arrive_columns
        
        table.setColumnCount(len(columns))

        for i in range(0, len(columns)):
            column_title = columns[i]['title']
            header_item = QtGui.QTableWidgetItem(column_title)
            table.setHorizontalHeaderItem(i, header_item)
                
        if len(arrive_list) != 0:
            table.setRowCount(len(arrive_list))
            
            for i in range(0, len(arrive_list)):
                for j in range(0, len(columns)):
                    self.fill_cell(i, j, columns[j]['name'], arrive_list[i])
            
            arrive_foto = arrive_list[0].foto
            
            if arrive_foto != None:
                self.fill_arrive_foto(arrive_foto)

    def fill_cell(self, row, col, column_name, record):
        column_value = getattr(record, column_name)
        
        if (column_name == 'is_cure') and (column_value == 1):
            value = u'Да'
        elif (column_name == 'is_cure') and (column_value == 0):
            value = u'Нет'
        elif column_name == 'leave_cause':
            value = record.leave_cause.cause
        elif column_name == 'send_address_id':
            column_value = record.send_address
            if column_value == None:
                value = u'нет'
            else:
                value = column_value.address
        elif (column_name == 'arrive_date') or (column_name == 'leave_date'):
            value = QDate(column_value).toString('dd.MM.yyyy')
        else:
            value = unicode(column_value)
            
        item = QtGui.QTableWidgetItem(value)
        self.ui.arriveTable.setItem(row, col, item)
        
        if col == 0:
            item.record = record
                
    def fill_arrive_foto(self, foto):
        scene = QtGui.QGraphicsScene()   
        
        fotopath = join(self.config['paths']['images'], foto)
        
        pixmap = (QtGui.QPixmap(fotopath).
                  scaledToHeight(self.ui.fotoArea.height()/1.12, 1).
                  scaledToWidth(self.ui.fotoArea.width()/1.2, 1))
        scene.addPixmap(pixmap)
        self.ui.fotoArea.setScene(scene)

    def update_table_slot(self, record, record_update_type):
        table = self.ui.arriveTable
        
        if record_update_type == 'create':
            table.setRowCount(table.rowCount()+1)
            columns = self.displayed_arrive_columns
            
            new_record_index = table.rowCount()-1
            
            for j in range(0, len(columns)):
                self.fill_cell(new_record_index, j, columns[j]['name'], record)
            
        else:
            for i in range(0, table.rowCount()):
                table_record = table.item(i, 0).record
                
                if record.id == table_record.id:
                    if record_update_type == 'update':
                        columns = self.displayed_arrive_columns
                        
                        for j in range(0, len(columns)):
                            self.fill_cell(i, j, columns[j]['name'], record)
                        
                    elif record_update_type == 'delete':
                        table.removeRow(i)
                    
                    break

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
        
    def change_arrive_foto(self, row, col):
        arrive_foto = self.ui.arriveTable.item(row, 0).record.foto
        
        if arrive_foto != None:
            self.fill_arrive_foto(arrive_foto)
        
    def open_arrive_record_slot(self, row=None, col=None):
        if (row == None) and (col == None):
            row = self.ui.arriveTable.currentRow()
            col = self.ui.arriveTable.currentColumn()
        
        table_item = self.ui.arriveTable.item(row, 0)
        record = table_item.record
        
        self.arriveDialog.open_arrive_record(record)
        
    def open_empty_arrive_slot(self):
        self.arriveDialog.db = self.db
        self.arriveDialog.open_empty_record(self.record.id)
 
    def delete_arrive_record_slot(self):
        selected_record_num = self.ui.arriveTable.currentRow()
        
        if selected_record_num != -1:
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

            if confirm == QtGui.QMessageBox.Ok:
                selected_row_index = self.ui.arriveTable.currentRow()
                record = self.ui.arriveTable.item(selected_row_index, 0).record
                
                try:
                    self.db.delete_record(record)
                except IOError:
                    sys.exit(IOError)
                
                if record.foto != None:
                    remove(join(self.config['paths']['images'], record.foto))
                    
                self.update_table_slot(record, 'delete')
                
    def close_button_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение закрытия',
            u"Вы уверены, что хотите закрыть форму?\nВсе введенные вами данные будут потеряны!", 
            QtGui.QMessageBox.Ok | 
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        if confirm == QtGui.QMessageBox.Ok:
            self.close()
        
        
class arriveDialog(QtGui.QDialog):
    tableUpdated = pyqtSignal(Arrive, str)
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = arrive_form.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowFlags(Qt.Window)
        
        self.ui.mainLayout = QtGui.QVBoxLayout(self)
        self.ui.mainLayout.addWidget(self.ui.fieldsBox)
        
        self.ui.fotoBox.setLayout(self.ui.fotoLayout)
        self.ui.mainLayout.addWidget(self.ui.fotoBox)
        
        self.ui.mainLayout.addWidget(self.ui.buttonBox)
        
        self.config = self.parent().config
        
        self.connect(self.ui.makeFoto, SIGNAL('clicked()'), self.make_foto_slot)
        self.connect(self.ui.openFoto, SIGNAL('clicked()'), self.open_foto_slot)
        self.connect(self.ui.saveButton, SIGNAL('clicked()'), self.save_record_slot)
        self.connect(self.ui.deleteButton, SIGNAL('clicked()'), self.delete_record_slot)
        self.connect(self.ui.closeButton, SIGNAL('clicked()'), self.close_slot)
        self.connect(self.ui.leave_cause_id, SIGNAL('activated(int)'), self.leave_cause_changed_slot)

    def database_opened_slot(self, database):
        self.close()
        self.db = database
        self.fill_cause_list()
        self.fill_send_address_list()
        
    def fill_cause_list(self):
        leave_cause_list_widget = self.ui.leave_cause_id
        leave_cause_list_widget.clear()
        
        cause_list = self.db.get_leave_cause_list()
        
        for i in range(0, len(cause_list)):
            leave_cause_list_widget.addItem(cause_list[i].cause, [cause_list[i].id, cause_list[i].with_address])
            
        leave_cause_list_widget.setCurrentIndex(0)
        
        if not cause_list[0].with_address:
            self.ui.send_address_id.setVisible(False)
            self.ui.send_address_id_label.setVisible(False)
    
    def fill_send_address_list(self):
        send_address_list_widget = self.ui.send_address_id
        send_address_list_widget.clear()
        
        send_address_list = self.db.get_send_addresses()
        
        for i in range(0, len(send_address_list)):
            send_address_list_widget.addItem(send_address_list[i].address, send_address_list[i].id)

    def clear_fields(self):
        self.ui.send_address_id_label.setVisible(False)
        self.ui.send_address_id.setVisible(False)
        
        columns = self.record.get_columns_names()
        
        for column_name in columns:
            if hasattr(self.ui, column_name):
                field = getattr(self.ui, column_name)
                
                if column_name == 'leave_cause_id':
                    field.setCurrentIndex(0)
                    with_address = field.itemData(0).toList()[1].toBool()

                    if with_address:
                        self.ui.send_address_id.setVisible(True)
                        self.ui.send_address_id_label.setVisible(True)
                else:
                    clear_field(field)
                
        scene = QtGui.QGraphicsScene()
        self.ui.fotoArea.setScene(scene)  
        
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
        
        columns = record.get_columns_names()
        
        for column in columns:
            record_field_value = getattr(record, column)
            
            if hasattr(self.ui, column):
                field = getattr(self.ui, column)
                
                if column == 'leave_cause_id':
                    if record.leave_cause.with_address:
                        self.ui.send_address_id.setVisible(True)
                        self.ui.send_address_id_label.setVisible(True)
                
                set_field_value(field, record_field_value)

            if(column == 'foto'):
                self.fill_arrive_foto(record_field_value) 
        
        self.state = 'open_record'
        self.show()
    
    def open_empty_record(self, person_id):
        self.record = Arrive({'person_id':person_id})
        self.clear_fields()
        self.ui.deleteButton.setEnabled(False)
        self.ui.saveButton.setText(u'Добавить')
        self.state = 'create_record'
        self.show()
    
    def get_images_directory(self):
        img_dir =  self.config['paths']['images']
        
        if not isdir(img_dir):
            mkdir(img_dir)
        
        return img_dir 
    
    def generate_image_filename(self):
        return unicode(QDate().currentDate().toString('dd-MM-yyyy') + '_' +
                       QTime().currentTime().toString('HH-mm-ss-zz') + '.png')
    
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
            fotoname = self.generate_image_filename()
            img_dir = self.get_images_directory()
            
            try:
                
                camera.saveSnapshot(join(img_dir, fotoname), timestamp=True)
            except IOError:
                sys.exit(IOError)
            
            if self.record.foto != None:
                remove(join(img_dir, self.record.foto))
                
            self.record.foto = fotoname
            
        self.fill_arrive_foto(fotoname)
   
    def open_foto_slot(self):
        path = unicode(QtGui.QFileDialog.getOpenFileName(self, u"Открыть фото", unicode(getcwdu()), u'Фотографии (*.png *.jpeg *.jpg *.gif)'))
    
        if path != '':
            fotoname = self.generate_image_filename()
            img_dir = self.get_images_directory()
            fotopath = join(img_dir, fotoname)
            
            try:
                src_image = Image.open(path, 'r')
                src_image.save(fotopath, 'PNG')
                
            except Exception:
                sys.exit(Exception.message)
            
            if self.record.foto != None:
                remove(img_dir, self.record.foto)
                
            self.record.foto = fotoname
         
            self.fill_arrive_foto(fotoname)
            
    def save_record_slot(self):
        if self.state == 'open_record':
            is_record_changed = False
            
            record = self.record
            columns = record.get_columns_names()
            
            for i in range(0, len(columns)):
                col_name = columns[i]
                
                if hasattr(self.ui, col_name):
                    field = getattr(self.ui, col_name)
                    old_value = getattr(self.record, col_name)
                    new_value = get_field_value(field)
                    
                    if old_value != new_value:
                        is_record_changed = True
                        setattr(record, col_name, new_value)
                        
            if is_record_changed:
                self.db.update_records()
                self.tableUpdated.emit(record, 'update')
        
        elif self.state == 'create_record':
            new_record = self.record
            values = {}
            
            columns = self.record.get_columns_names()
            for column_name in columns:
                if hasattr(self.ui, column_name):
                    field = getattr(self.ui, column_name)
                    values[column_name] = get_field_value(field)
                
            new_record.set_values(values)
        
            try:
                self.db.insert_record(new_record)
            except IOError:
                sys.exit(IOError)
            
            self.record = new_record
            self.tableUpdated.emit(new_record, 'create')
            
            self.state = 'open_record'            
            self.ui.saveButton.setText(u'Сохранить')
            self.ui.deleteButton.setEnabled(True)
     
    def fill_arrive_foto(self, foto):
        scene = QtGui.QGraphicsScene()
        
        fotopath = join(self.config['paths']['images'], foto)
        
        scene.addPixmap(QtGui.QPixmap(fotopath))
        self.ui.fotoArea.setScene(scene)
 
    def delete_record_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
            u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
            QtGui.QMessageBox.Ok | 
            QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

        if confirm == QtGui.QMessageBox.Ok:
            self.db.delete_record(self.record)
            
            if self.record.foto != None:
                remove(join(self.config['paths']['images'], self.record.foto))
                
            self.tableUpdated.emit(self.record, 'delete')
        
    def close_slot(self):
        confirm = QtGui.QMessageBox.question(self, u'Подтверждение закрытия формы',
                u"Вы уверены что хотите закрыть форму?\nВсе введенные данные будут потеряны", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
    
        if confirm == QtGui.QMessageBox.Ok:
            if self.state == 'create_record' and self.record.foto != None:
                tmp_fotoname = self.record.foto
                remove('images/%s' % tmp_fotoname)
            
            self.hide()
    
    def leave_cause_changed_slot(self, item_index):
        widget = self.ui.leave_cause_id
        item_data = widget.itemData(item_index).toList()
        
        is_with_address = item_data[1].toBool()
        
        if is_with_address:
            self.ui.send_address_id.setVisible(True)
            self.ui.send_address_id_label.setVisible(True)
            self.ui.send_address_id.setCurrentIndex(0)
        else:
            self.ui.send_address_id.setVisible(False)
            self.ui.send_address_id_label.setVisible(False)
            self.ui.send_address_id.setCurrentIndex(-1)


class filterDialog(QtGui.QDialog):
    tableFiltered = pyqtSignal(Query)
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = filter_form.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowFlags(Qt.Tool)
        
        self.filtering_columns = ([
            {'name':'last_name',            'field_name':'last_name',               'with_type_check':True},
            {'name':'first_name',           'field_name':'first_name',              'with_type_check':True},
            {'name':'middle_name',          'field_name':'middle_name',             'with_type_check':True},
            {'name':'gender',               'field_name':'gender',                  'with_type_check':False},
            {'name':'passport_series',      'field_name':'passport_series',         'with_type_check':False},
            {'name':'passport_number',      'field_name':'passport_number',         'with_type_check':False},
            {'name':'born_place',           'field_name':'born_place',              'with_type_check':True},
            {'name':'born_date',            'field_name':('born_date_from', 
                                                          'born_date_to'),          'with_type_check':False},
            {'name':'address',              'field_name':'address_city',            'with_type_check':False},
            {'name':'address',              'field_name':'address',                 'with_type_check':True},
            {'name':'addiction_id',         'field_name':'addiction_type',          'with_type_check':False},
            {'name':'addiction_start_date', 'field_name':('addiction_duration_from',
                                                          'addiction_duration_to'),  'with_type_check':False},
                                   ])
        
        self.connect(self.ui.closeButton, SIGNAL('clicked()'), self.close)
        self.connect(self.ui.filterButton, SIGNAL('clicked()'), self.filter_slot)
        self.connect(self.ui.resetButton, SIGNAL('clicked()'), self.reset_filter_slot)
        self.connect(self.ui.born_date_enabled, SIGNAL('stateChanged(int)'), self.switch_born_date)

    def database_opened_slot(self, database):
        self.close()
        self.db = database
        self.fill_addiction_list()
        self.clear_fields()

    def clear_fields(self):
        columns = self.filtering_columns
        
        for column in columns:
            column_name = column['name']
            
            if column_name == 'gender':
                self.ui.male.setChecked(True)
                self.ui.female.setChecked(True)
            elif column_name == 'born_date' or column_name == 'addiction_start_date':
                first_field  = getattr(self.ui, column['field_name'][0])
                second_field = getattr(self.ui, column['field_name'][1])
                
                clear_field(first_field)
                clear_field(second_field)
                
                if column_name == 'born_date':
                    self.ui.born_date_enabled.setChecked(False)
            else:
                field = getattr(self.ui, column['field_name'])
                clear_field(field)
                
                if column['with_type_check']:
                    type_field = getattr(self.ui, column['field_name'] + '_type')
                    clear_field(type_field)

    def filter_slot(self):
        columns = self.filtering_columns
        
        query = self.db.get_person_list_query()
        
        for column in columns:
            column_name = column['name']
            field_name = column['field_name']
        
            if column_name == 'gender':
                if self.ui.male.isChecked() and self.ui.female.isChecked():
                    query = query.filter("(gender=:male_gender or gender=:female_gender)").params(male_gender=Person.male, female_gender=Person.female)
                    
                elif self.ui.male.isChecked():
                    query = query.filter("gender=:male_gender").params(male_gender=Person.male)
                    
                elif self.ui.female.isChecked():
                    query = query.filter("gender=:female_gender").params(female_gender=Person.female)
                    
            elif column_name == 'born_date':
                if self.ui.born_date_enabled.isChecked():
                    from_date = get_field_value(getattr(self.ui, field_name[0]))
                    to_date = get_field_value(getattr(self.ui, field_name[1]))
                    
                    query = query.filter("(date(born_date) between :from_date and :to_date)").params(from_date=from_date, to_date=to_date)
                
            elif column_name == 'addiction_start_date':
                addiction_duration_from = get_field_value(getattr(self.ui, field_name[0]))
                addiction_duration_to   = get_field_value(getattr(self.ui, field_name[1]))
                
                if (addiction_duration_from == '') and (addiction_duration_to != ''):
                    addiction_duration_from = 0
                    addiction_duration_to = int(addiction_duration_to)
                    
                if (addiction_duration_from != '') and (addiction_duration_to == ''):
                    addiction_duration_from = int(addiction_duration_from)
                    addiction_duration_to   = addiction_duration_from
                
                if (addiction_duration_from != '') and (addiction_duration_to != ''):
                    addiction_duration_from = int(addiction_duration_from)
                    addiction_duration_to   = int(addiction_duration_to)
                
                if (addiction_duration_from != '') or (addiction_duration_to != ''):
                    query = (query.filter("((date('now') - date(addiction_start_date)) between :duration_from and :duration_to)")
                                  .params(duration_from=addiction_duration_from, duration_to=addiction_duration_to))
            else:
                value = get_field_value(getattr(self.ui, field_name))
                if value != '' and value != None and value != -1:
                    if column['field_name'] == 'address_city':
                        type = 'like'
                    elif column['with_type_check']:
                        type_field = getattr(self.ui, field_name+'_type')
                        if type_field.isChecked():
                            type = 'where'
                        else:
                            type = 'like'
                    else:
                        type = 'where'
                        
                    if type == 'like':
                        query = query.filter("lower(%s) like lower(:%s)" % (column_name, column_name)).params(**{column_name:'%%%s%%' % value})
                    elif type == 'where':
                        if value.__class__.__name__ == 'str' or value.__class__.__name__ == 'unicode':
                            query = query.filter("lower(%s)=lower(:%s)" % (column_name, column_name)).params(**{column_name:value})
                        else:
                            query = query.filter("%s=:%s" % (column_name, column_name)).params(**{column_name:value})
                    
        self.tableFiltered.emit(query)

    def reset_filter_slot(self):
        self.clear_fields()
        self.tableFiltered.emit(self.db.get_person_list_query())

    def fill_addiction_list(self):
        addiction_list = self.db.get_addictions()
        widget = self.ui.addiction_type
        widget.clear()
        
        widget.addItem(u'Все', -1)
        
        for addiction in addiction_list:
            widget.addItem(addiction.name, addiction.id)

        widget.setCurrentIndex(0)
    
    def switch_born_date(self, state):
        state = bool(state)
        self.ui.born_date_from.setEnabled(state)
        self.ui.born_date_to.setEnabled(state)
        self.ui.born_date_label.setEnabled(state)
        self.ui.born_date_label_from.setEnabled(state)
        self.ui.born_date_label_to.setEnabled(state)
    
    
class catalogsDialog(QtGui.QDialog):
    addictionsChanged = pyqtSignal()
    addressesChanged  = pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = catalogs_form.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowFlags(Qt.Window)
        
        self.mainLayout = QtGui.QVBoxLayout(self)
        self.mainLayout.addWidget(self.ui.tabs)
        
        self.ui.addictionTab.setLayout(self.ui.addictionLayout)
        self.ui.addressTab.setLayout(self.ui.addressLayout)
        
        self.connect(self.ui.addAddiction,    SIGNAL('clicked()'), self.add_addiction)
        self.connect(self.ui.editAddiction,   SIGNAL('clicked()'), self.update_addiction)
        self.connect(self.ui.deleteAddiction, SIGNAL('clicked()'), self.delete_addiction)
        
        self.connect(self.ui.addAddress,    SIGNAL('clicked()'), self.add_address)
        self.connect(self.ui.editAddress,   SIGNAL('clicked()'), self.update_address)
        self.connect(self.ui.deleteAddress, SIGNAL('clicked()'), self.delete_address)
        
        self.connect(self.ui.addictionTable, SIGNAL('cellDoubleClicked(int, int)'), self.update_addiction)
        
    def database_opened_slot(self, database):
        self.close()
        self.db = database
        self.fill_addiction_table()
        self.fill_send_address_table()
    
    def fill_addiction_table(self):
        addiction_list = self.db.get_addictions()
        
        table = self.ui.addictionTable
        table.clear()
        table.setRowCount(len(addiction_list))
        
        for i in range(0, len(addiction_list)):
            item = QtGui.QTableWidgetItem(addiction_list[i].name)
            table.setItem(i, 0, item)
            
            item.record = addiction_list[i]
    
    def fill_send_address_table(self):
        address_list = self.db.get_send_addresses()
        
        table = self.ui.addressTable
        table.clear()
        table.setRowCount(len(address_list))
        
        for i in range(0, len(address_list)):
            item = QtGui.QTableWidgetItem(address_list[i].address)
            table.setItem(i, 0, item)
            
            item.record = address_list[i]

    def add_addiction(self):
        new_addiction_name, confirm = QtGui.QInputDialog.getText(self, u'Добавление вида зависимости', 
                                                                       u'Введите название нового вида зависимости:')

        if confirm:
            addiction = Addiction(unicode(new_addiction_name))
            self.db.insert_record(addiction)
            
            self.fill_addiction_table()
            self.addictionsChanged.emit()
    
    def update_addiction(self):
        current_index = self.ui.addictionTable.currentRow()
        
        if current_index != -1:
            table_item = self.ui.addictionTable.item(current_index, 0)
            record = table_item.record
            
            new_addiction_name, confirm = QtGui.QInputDialog.getText(self, u'Изменение вида зависимости', 
                                                                           u'Введите новое название вида зависимости:', text=record.name)
    
            if confirm:
                record.name = unicode(new_addiction_name)
                self.db.update_records()
                table_item.setText(new_addiction_name)
                
                self.addictionsChanged.emit()
    
    def delete_addiction(self):
        current_index = self.ui.addictionTable.currentRow()
        if current_index != -1:
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
    
            if confirm == QtGui.QMessageBox.Ok:
                    record = self.ui.addictionTable.item(current_index, 0).record
                    
                    addicted_count = len(record.addicted)
                    
                    if addicted_count == 0:
                        self.db.delete_record(record)
                        self.ui.addictionTable.removeRow(current_index)
                        self.addictionsChanged.emit()
                    else:
                        QtGui.QMessageBox.question(self, u'Ошибка',
                            u"Невозможно удалить запись. В базе остались люди с этой зависимостью.\n", 
                            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
    
    def add_address(self):
        new_address_name, confirm = QtGui.QInputDialog.getText(self, u'Добавление адреса', 
                                                                     u'Введите новый адрес:')

        if confirm:
            addiction = SendAddress(unicode(new_address_name))
            self.db.insert_record(addiction)
            
            self.fill_send_address_table()
            self.addressesChanged.emit()
    
    def update_address(self):
        current_index = self.ui.addressTable.currentRow()
        
        if current_index != -1:
            table_item = self.ui.addressTable.item(current_index, 0)
            record = table_item.record
            
            new_address_name, confirm = QtGui.QInputDialog.getText(self, u'Изменение адреса', 
                                                                           u'Введите новый адрес:', text=record.address)
    
            if confirm:
                record.address = unicode(new_address_name)
                self.db.update_records()
                table_item.setText(new_address_name)
                
                self.addressChanged.emit()
    
    def delete_address(self):
        current_index = self.ui.addressTable.currentRow()
        if current_index != -1:
            confirm = QtGui.QMessageBox.question(self, u'Подтверждение удаления',
                u"Вы уверены, что хотите удалить запись?\nВосстановить ее можно будет только из бэкапа", 
                QtGui.QMessageBox.Ok | 
                QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
    
            if confirm == QtGui.QMessageBox.Ok:
                    record = self.ui.addressTable.item(current_index, 0).record
                    
                    causes_count = record.causes
                    
                    if len(causes_count) == 0:
                        self.db.delete_record(record)
                        self.ui.addressTable.removeRow(current_index)
                        self.addressesChanged.emit()
                    else:
                        QtGui.QMessageBox.question(self, u'Ошибка',
                            u"Невозможно удалить запись.\nВ базе остались записи прихода/ухода с этим адресом отправки.", 
                            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
                        

if __name__ == '__main__':    
    app = Application()
    app.execute()