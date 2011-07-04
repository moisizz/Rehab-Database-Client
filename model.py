# -*- coding: utf8 -*-

'''
Created on 30.06.2011

@author: Моисеев Данил
'''

import sqlite3

class Model(object):
    '''Класс предназначен для взаимодействия с базой'''

    def __init__(self, params):
        self.create_connection(params['database_path'])
        
        
        #Если title у колонки пустой, значит в таблице она не будет отображаться
        self.person_schema = \
        [ {'col_name': 'id',                    'title': u'№ договора',              'type': 'INTEGER PRIMARY KEY'},
          {'col_name': 'contract_date',         'title': u'Дата договора',           'type': 'TEXT'},
          {'col_name': 'last_name',             'title': u'Фамилия',                 'type': 'TEXT'},
          {'col_name': 'first_name',            'title': u'Имя',                     'type': 'TEXT'},
          {'col_name': 'middle_name',           'title': u'Отчество',                'type': 'TEXT'},
          {'col_name': 'gender',                'title': u'Пол',                     'type': 'TEXT'},
          {'col_name': 'born_date',             'title': u'Дата рождения',           'type': 'TEXT'},
          {'col_name': 'born_place',            'title': u'Место рождения',          'type': 'TEXT'},
          {'col_name': 'passport_series',       'title': u'Серия паспорта',          'type': 'TEXT'},
          {'col_name': 'passport_number',       'title': u'Номер паспорта',          'type': 'TEXT'},
          {'col_name': 'passport_given',        'title': u'Паспорт выдан',           'type': 'TEXT'},
          {'col_name': 'address',               'title': u'Адрес',                   'type': 'TEXT'},
          {'col_name': 'contact_phone',         'title': u'Контакт. телефон',        'type': 'TEXT'},
          {'col_name': 'contact_person',        'title': u'Контакт. лицо',           'type': 'TEXT'},
          {'col_name': 'addiction_start_date',  'title': u'Дата начала зависимости', 'type': 'TEXT'},
          {'col_name': 'addiction_type',        'title': u'Вид зависимости',         'type': 'INTEGER'},
          {'col_name': 'notes',                 'title': u'Примечания',              'type': 'TEXT'}]
        
        self.arrive_schema = \
        [{'col_name':'id',          'title': '',               'type': 'INTEGER PRIMARY KEY'},
         {'col_name':'person_id',   'title': '',               'type': 'INTEGER'},
         {'col_name':'arrive_date', 'title': u'Прибыл',         'type': 'TEXT'},
         {'col_name':'leave_date',  'title': u'Убыл',           'type': 'TEXT'},
         {'col_name':'leave_cause', 'title': u'Причина',        'type': 'TEXT'},
         {'col_name':'is_cure',     'title': u'Долечился ли',   'type': 'BOOLEAN'},
         {'col_name':'foto',        'title': '',               'type': 'TEXT'},]
        
        self.addiction_schema = \
        [{'col_name': 'id',    'title': '',      'type': 'INTEGER PRIMARY KEY'},
         {'col_name': 'name',  'title': u'Текст', 'type': 'TEXT'}]
        
    def create_connection(self, database_path):
        '''Создает новое соединение и курсор'''
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()

    def close_connection(self):
        '''Закрывает курсор и соединение с базой'''
        self.cursor.close()
        self.conn.close()
    
    def clear_database(self):
        '''Удаляет текущие таблицы'''
        self.cursor.execute('drop table if exists person')
        self.cursor.execute('drop table if exists arrive')
        self.cursor.execute('drop table if exists addiction')
        self.conn.commit()
        
    def create_empty_tables(self):
        '''Создает новую пустую базу'''
        
        #Создаем пустые таблицы
        schemas = {'person': self.person_schema, 'arrive': self.arrive_schema, 'addiction': self.addiction_schema}
        for key in schemas.keys():        
            fields_string = ''
            
            #Создаем запросы
            for i in range(0, len(schemas[key])):
                row = schemas[key][i]
                fields_string += '%s %s' % (row['col_name'], row['type'])
                if i != (len(schemas[key])-1):
                    fields_string += ','
                  
            #Выполняем запросы  
            self.cursor.execute('CREATE TABLE %s (%s);' % (key, fields_string))
            
        #Заполняем таблицы видов зависимости
        addictions = [u'алкоголь', u'наркотики', u'дизоморфин', u'прочее']
        
        for addiction in addictions:
            self.cursor.execute('insert into addiction (name) values ("%s")' % addiction)
        
        self.conn.commit()
        
    def insert_record(self, table_name, values_dict):
        record_names  = tuple(values_dict.keys())
        record_values = tuple(values_dict.values())
        
        placeholder_string = ''
        for i in range(0, len(values_dict)):
            placeholder_string += '?'
            if i != (len(values_dict)-1):
                placeholder_string += ','
                
        placeholder_string = '(%s)' % placeholder_string
        
        query_string = 'insert into %s %s values %s' % (table_name,
                                                        record_names, 
                                                        placeholder_string)
        
        self.cursor.execute(query_string, record_values)
        self.conn.commit()
        
        return self.cursor.execute('select * from %s order by id desc limit 1' % table_name).fetchone()

    def update_record(self, table_name, id, values_dict):
        record_values = tuple(values_dict.values())
        
        new_values_string = ''
        
        column_num = 0
        
        for column_name in values_dict.keys():
            new_values_string += '%s=?' % column_name
            if(column_num != len(values_dict)-1):
                new_values_string += ', '
            column_num += 1
        
        query_string = 'update or rollback %s set %s where id=%s' % (table_name, new_values_string, id)
        self.cursor.execute(query_string, record_values)
        self.conn.commit()
        
        return self.cursor.execute('select * from %s where id=%s limit 1' % (table_name, id)).fetchone()

    def delete_record(self, table_name, id):
        self.cursor.execute('delete from %s where id=%s' % (table_name, id))
        self.conn.commit()
            
    def get_person_list(self, filter_params={}):
        query_string = 'select * from person '
        
        i = 1
        
        if len(filter_params) != 0:
            for key in filter_params.keys():
                query_string += 'where %s=%s' % (key, filter_params[key])
                if (i != len(filter_params)):
                    query_string += ' and '

        return self.cursor.execute(query_string).fetchall()

    def get_person(self, id):
        person = self.cursor.execute('select * from person where id=?', (id, )).fetchone()
        
        return person
        
    def get_arrive_list(self, person_id):
        return self.cursor.execute('select * from arrive where person_id=?', (person_id, )).fetchall()
    
    def get_arrive(self, id):
        pass
    
    def get_addictions(self):
        return self.cursor.execute('select * from addiction').fetchall()
        
if __name__ == '__main__':
    db = Model({'database_path':'database.db'})
    db.clear_database()
    db.create_empty_tables()
    
    person = {'contract_date':'10.10.2010', 
              'last_name':u'Пертов', 
              'first_name':u'Сергей', 
              'middle_name':u'Викторович', 
              'gender':'male', 
              'born_date':'11.11.1960', 
              'born_place':u'г. Чайковский', 
              'passport_series':'2345', 
              'passport_number':'346345',
              'passport_given':u'Чайковским ГОВД', 
              'address':u'ул. Советская, д. 4, кв. 56', 
              'contact_phone':'1-23-45', 
              'contact_person':u'сестра Людмила', 
              'addiction_start_date':'10.10.2008', 
              'addiction_type': 2, 
              'notes':u'Разные примечания'}
    
    arrive1 = {'person_id':1, 'arrive_date':'01.01.2009', 'leave_date':'02.02.2009', 'leave_cause':u'ушел',      'is_cure': False,  'foto':'fotka1.png'}
    arrive2 = {'person_id':1, 'arrive_date':'01.01.2010', 'leave_date':'02.02.2010', 'leave_cause':u'ушел',      'is_cure': False,  'foto':'fotka2.png'}
    arrive3 = {'person_id':1, 'arrive_date':'01.01.2011', 'leave_date':'02.02.2011', 'leave_cause':u'долечился', 'is_cure': True,   'foto':'fotka3.png'}

    db.insert_record('person', person)
    db.insert_record('arrive', arrive1)
    db.insert_record('arrive', arrive2)
    db.insert_record('arrive', arrive3)