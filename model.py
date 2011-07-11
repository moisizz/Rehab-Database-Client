# -*- coding: utf8 -*-

import sqlite3
import copy

from datetime import datetime

from datetime import date
from random import choice, randrange
from time import time

from sqlalchemy import create_engine, Table, Column, Integer, Unicode, UnicodeText, SmallInteger, Date, DateTime, MetaData, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relation, backref, eagerload
from sqlalchemy.ext.declarative import declarative_base
        
Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    
    male   = 1
    female = 2

    id = Column(Integer, primary_key=True)
    contract_number = Column(Unicode)
    contract_date = Column(Date)
    last_name = Column(Unicode)
    first_name = Column(Unicode)
    middle_name = Column(Unicode)
    gender = Column(Integer)
    born_date = Column(Date())
    born_place = Column(Unicode)
    passport = Column(Unicode)
    passport_given = Column(Unicode)
    address = Column(Unicode)
    contact_phone = Column(Unicode)
    contact_person = Column(Unicode)
    addiction_start_date = Column(Date)
    addiction_id = Column(Integer, ForeignKey('addiction.id', ondelete='RESTRICT'), nullable=True)
    notes = Column(UnicodeText)

    arrives = relation("Arrive", order_by="Arrive.arrive_date", uselist=True, cascade='all, delete-orphan')
    addiction = relation("Addiction", order_by="Addiction.name", uselist=False, backref='addicted')

    def __init__(self, values):
        self.set_values(values)
        
    def __repr__(self):
        return u"Человек<(%s, %s, %s, %s, %s, %s)>" % (self.last_name, self.first_name, self.middle_name, self.born_date, self.born_place, self.passport)

    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])

    def get_columns_names(self):
        return self.__table__.columns.keys()


class Arrive(Base):
    __tablename__ = 'arrive'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    arrive_date = Column(Date)
    leave_date = Column(Date)
    leave_cause_id = Column(Integer, ForeignKey('leave_cause.id', ondelete='RESTRICT'), nullable=True)
    send_address_id = Column(Integer, ForeignKey('send_address.id', ondelete='RESTRICT'), nullable=True)
    is_cure = Column(Boolean)
    foto = Column(Unicode)

    leave_cause = relation("LeaveCause", order_by="LeaveCause.cause", uselist=False)
    send_address = relation("SendAddress", order_by="SendAddress.address", uselist=False, backref='causes')

    def __init__(self, values):
        self.set_values(values)
        
    def set_values(self, values):
        for key in values.keys():
            setattr(self, key, values[key])
        
    def __repr__(self):
        return "<Arrive('%s','%s', %s, '%s')>" % (self.arrive_date, self.leave_date, self.leave_cause, self.foto)
    
    def get_columns_names(self):
        return self.__table__.columns.keys()


class Addiction(Base):
    __tablename__ = 'addiction'
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)

    def __init__(self, name):
        self.name = name
                
    def __repr__(self):
        return "<Addiction('%s')>" % (self.name)
    
    def get_columns_names(self):
        return self.__table__.columns.keys()


class LeaveCause(Base):
    __tablename__ = 'leave_cause'
    
    id = Column(Integer, primary_key=True)
    cause = Column(Unicode)
    with_address = Column(Boolean)
        
    def __init__(self, cause, with_address):
        self.cause = cause
        self.with_address = with_address
        
    def __repr__(self):
        return "<Arrive('%s')>" % (self.cause)
    
    def get_columns_names(self):
        return self.__table__.columns.keys()


class SendAddress(Base):
    __tablename__ = 'send_address'
    
    id = Column(Integer, primary_key=True)
    address = Column(Unicode, nullable=False)
    
    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return "<Arrive('%s')>" % (self.address)
    
    def get_columns_names(self):
        return self.__table__.columns.keys()

def database_lower_function(str):
    if str != None:
        return str.lower()
    else:
        return ''


class Model(object):
    '''Класс предназначен для взаимодействия с базой'''

    def __init__(self, params):
        self.create_connection(params['database_path'])
        
    def create_connection(self, database_path):
        '''Создает новое соединение'''
        self.engine = create_engine('sqlite:///%s' % database_path, echo=False)
        self.conn = self.engine.connect()
        
        self.conn.connection.create_function('lower',1, database_lower_function)
        
        self.session = sessionmaker(bind=self.conn)()
        self.person_metadata = Person.metadata
        self.arrive_metadata = Arrive.metadata
        self.leave_cause_metadata = LeaveCause.metadata
        self.addiction_metadata = Addiction.metadata
        self.send_address_metadata = SendAddress.metadata

    def close_connection(self):
        '''Закрывает соединение с базой'''
        self.session.close()
    
    def create_empty_tables(self):
        '''Создает новые пустые базы'''   
        self.person_metadata.drop_all(self.engine)
        self.arrive_metadata.drop_all(self.engine)
        self.send_address_metadata.drop_all(self.engine)
        self.addiction_metadata.drop_all(self.engine)
        self.leave_cause_metadata.drop_all(self.engine)
             
        self.person_metadata.create_all(self.engine)
        self.arrive_metadata.create_all(self.engine)
        self.send_address_metadata.create_all(self.engine)
        self.addiction_metadata.create_all(self.engine)
        self.leave_cause_metadata.create_all(self.engine)
        
        addictions = [Addiction(u'Наркотики'), Addiction(u'Дезоморфин'), Addiction(u'Прочее'), Addiction(u'Табак')]
        send_addresses = [SendAddress(u'Екатеринбург'), SendAddress(u'Чайковский-Завьялово'), 
                          SendAddress(u'Чайковский-Рубеж'), SendAddress(u'Пермь'), 
                          SendAddress(u'Воткинск'), SendAddress(u'Ижевск-Мингазин'), SendAddress(u'Ижевск-Каримов')]
        leave_causes = [LeaveCause(u'Нет', False), LeaveCause(u'Самоуход', False), LeaveCause(u'Отправлен в адаптацию', True)]

        self.session.add_all(addictions)
        self.session.add_all(send_addresses)
        self.session.add_all(leave_causes)
        self.session.commit()
        
    def insert_record(self, record_object):
        self.session.add(record_object)
        self.session.commit()
    
    def update_records(self):
        self.session.commit()
    
    def delete_record(self, record):
        self.session.delete(record)
        self.session.commit()
    
    def get_person_list_query(self):
        return self.session.query(Person)
    
    def get_person_list(self):
        return self.get_person_list_query().all()
    
    def get_addictions(self):
        return self.session.query(Addiction).order_by(Addiction.name).all()

    def get_send_addresses(self):
        return self.session.query(SendAddress).order_by(SendAddress.address).all()

    def get_leave_cause_list(self):
        return self.session.query(LeaveCause).order_by(LeaveCause.cause).all()

def generate_db(db, record_count):
    db.create_empty_tables()
    
    db.person_metadata.drop_all(db.engine)
    db.arrive_metadata.drop_all(db.engine)
    db.send_address_metadata.drop_all(db.engine)
    db.addiction_metadata.drop_all(db.engine)
    db.leave_cause_metadata.drop_all(db.engine)
         
    db.person_metadata.create_all(db.engine)
    db.arrive_metadata.create_all(db.engine)
    db.send_address_metadata.create_all(db.engine)
    db.addiction_metadata.create_all(db.engine)
    db.leave_cause_metadata.create_all(db.engine)
    
    male_first_names = [u'Сергей', u'Юрий', u'Петр', u'Василий', u'Степан', u'Павел', u'Владимир']
    female_first_names = [u'Татьяна', u'Анастасия', u'Любовь', u'Полина', u'Алевтина']
    
    male_middle_names = [u'Юрьевич', u'Сергеевич', u'Петрович', u'Степанович', u'Павлович', u'Владимирович'] 
    female_middle_names = [u'Юрьевна', u'Сергеевна', u'Петровна', u'Степановна', u'Павловна', u'Владимировна']
    
    male_last_names = [u'Иванов', u'Петров', u'Сергеев', u'Сидоров', u'Васильев']
    female_last_names = [u'Иванова', u'Петрова', u'Сергеева', u'Сидорова', u'Васильева'] 
    
    session = db.session

    born_places = [u'г. Чайковский', u'г. Пермь', u'село Ольховка', u'село Барда', u'г. Березники', u'г. Лысьва', u'г. Чусовой']
    addresses = [u'г. Чайковский ул. Сосновая 5, кв. 4', u'г. Пермь, ул. Карла-Маркса 3\\2, кв. 6', u'г. Чайковский']

    addictions = [Addiction(u'Наркотики'), Addiction(u'Дезоморфин'), Addiction(u'Прочее'), Addiction(u'Табак')]
    
    send_addresses = [SendAddress(u'Екатеринбург'), SendAddress(u'Чайковский-Завьялово'), 
                      SendAddress(u'Чайковский-Рубеж'), SendAddress(u'Пермь'), 
                      SendAddress(u'Воткинск'), SendAddress(u'Ижевск-Мингазин'), SendAddress(u'Ижевск-Каримов')]

    leave_causes = [LeaveCause(u'Самоуход', False), LeaveCause(u'Отправлен в адаптацию', True)]
    
    session.add_all(addictions)
    session.add_all(send_addresses)
    session.add_all(leave_causes)
    
    persons = []
    
    for i in range(0, record_count):
        
        gender = randrange(1, 3)
        
        if(gender == Person.male):
            last_name = choice(male_last_names)
            first_name = choice(male_first_names)
            middle_name = choice(male_middle_names)
        else:
            last_name = choice(female_last_names)
            first_name = choice(female_first_names)
            middle_name = choice(female_middle_names)
        
        person = Person({'contract_number':i,
                         'last_name':last_name,
                         'first_name':first_name,
                         'middle_name':middle_name,
                         'gender':gender,
                         'born_date':date(randrange(1950, 2000), randrange(1, 13), randrange(1, 28)),
                         'born_place':choice(born_places),
                         'passport':unicode(randrange(1111, 9999)) + u'№' + unicode(randrange(111111, 999999)),
                         'passport_given':u'Чайковским ГОВД',
                         'address':choice(addresses), 
                         'contact_phone':u'1-23-45',
                         'contact_person':u'Сестра',
                         'addiction_start_date':date(randrange(2000, 2010), randrange(1, 13), randrange(1, 28)),
                         'notes':u'Большой текст с разными примечаниями'})
        
        person.addiction = choice(addictions)
        
        arrive1 = Arrive({'arrive_date':date(2009, 5, 5), 'leave_date':date(2009, 6, 6),  'is_cure':False, 'foto':u'foto1.png'})
        arrive1.leave_cause = leave_causes[0]
        
        arrive2 = Arrive({'arrive_date':date(2009, 5, 5), 'leave_date':date(2009, 6, 6),  'is_cure':False, 'foto':u'foto2.png'})
        arrive2.leave_cause = leave_causes[0]
        
        arrive3 = Arrive({'arrive_date':date(2009, 5, 5), 'leave_date':date(2009, 6, 6),  'is_cure':True, 'foto':u'foto3.png'})
        arrive3.leave_cause = leave_causes[1]
        arrive3.send_address = choice(send_addresses)
        
        person.arrives = [arrive1, arrive2, arrive3]
        
        persons.append(person)
        
    session.add_all(persons)
    session.commit()
    
if __name__ == '__main__':
    #t = time()
    db = Model({'database_path':'small_test_database.db'})
    generate_db(db, 30)
    """
    print "Время открытия = %s" % (time() - t)
    t = time()
    l = db.get_person_list()
    print "Время запроса = %s" % (time() - t)
    
    t = time()
    for row in l:
        print row, '|', row.addiction.name, '|', row.arrives[0].leave_cause.cause, row.arrives[1].leave_cause.cause, row.arrives[2].leave_cause.cause
    print "Время отображения = %s" % (time() - t)
    
    print Person.__table__.columns.keys()"""
    
