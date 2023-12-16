import sqlalchemy
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import pytz
metadata_obj = MetaData()

Base = declarative_base()

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__%(all_column_names)s__'
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

metadata = sqlalchemy.MetaData(naming_convention=convention)

class Users(Base):
    __tablename__ = 'users'
    metadata = metadata_obj
    id = Column(Integer, primary_key=True)
    name = Column('name/login', String)

    def __init__(self, name):
        # self.id = id
        self.name = name

    def __repr__(self):
        return f'({self.id} {self.name})'

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

class Passwords(Base):
    __tablename__ = 'passwords'
    metadata = metadata_obj
    user_id = Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
    password = Column('passwords', String)

    def __init__(self, user_id, password):
        # self.id = id
        self.user_id = user_id
        self.password = password

    def __repr__(self):
        return f'({self.user_id} {self.password})'

    def get_user_id(self):
        return self.user_id

    def get_pass(self):
        return self.password


class Messages(Base):
    __tablename__ = 'messages'
    metadata = metadata_obj
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    body = Column('messages', String)
    created_at = Column('date', DateTime(timezone=True))

    def __init__(self, user_id, body, created_at):
        # self.id = id
        self.user_id = user_id
        self.body = body
        self.created_at = created_at

    def __repr__(self):
        return f'{db.query(Users).filter_by(id=self.user_id)[0].get_name()}: {self.body} ({self.created_at})'

    def get_user_id(self):
        return self.user_id


engine = create_engine('sqlite:///user_names.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine) # Class
db = Session() #instance

# print(engine.url.render_as_string(hide_password=False))



# di = db.query(Users).filter_by(name='aloha').all()
# d = di[0]
# print(d.get_id())
# print(db.query(Messages).all())
#
# dic = db.query(Users).filter_by(name='alora').all()
# print(dic)
#
# dic1 = db.query(Users).filter_by(name='alora').all()
# for i in dic1:
#     print(i.get_id())
# # for i in dic:
#     print(i)
#     for j in i:
#         print(j)
# print(d)

# x = 'aloha'
# y = 'as1214'
# print(db.query(Users, Passwords).filter(Users.id == Passwords.user_id).filter(Passwords.password == y).all())
# print(db.query(Users, Passwords).filter(Users.id == Passwords.user_id).filter(Users.name == x).filter(Passwords.password == y).all() != [])



# print(session.query(Users).filter(Users.name == 'asd').all())

# user1 = Users('alora')
# user2 = Users('aboba')
# user3 = Users('aloha')
# user4 = Users('abzhora')
# user5 = Users('mamont')


# db.add(user1)
# db.add(user2)
# db.add(user3)
# db.add(user4)
# db.add(user5)
# db.commit()
#
#
# p1 = Passwords(1, 'asdasd')
# p2 = Passwords(2, 'asasfsdasd')
# p3 = Passwords(3, 'as1214')
# p4 = Passwords(4, 'adxz cz')
# p5 = Passwords(5, 'asdasd')
#
# db.add(p1)
# db.add(p2)
# db.add(p3)
# db.add(p4)
# db.add(p5)
# db.commit()

# result = db.query(Users, Passwords).filter(Users.id == Passwords.user_id)
#
# for r in result:
#     print(r)
#
# stmt = (
#     update(Users)
#     .where(Users.id == 1)
#     .values(id = 7)
# )
#
# db.commit()
#
# for r in result:
#     print(r)


# password_name = db.query(Users).filter(Users.name == 'aloha')

# print(password_name[1])
# for i in password_name:
#     print('__' * 8)
#     print(type(i))
#     print('__' * 8)
#     print(i)

# query = Passwords(password_name)
#
# db.add(password)
# db.commit()




#result = db.query(Users).all() #запрос на получение всех срочек

#result = db.query(Users).filter(Users.name == 'alora') #запрос на получение строчек только по фильтру. result будет
                                                            # типа query, поэтому вывод надо делать через цикл

#result = db.query(Users).filter(Users.name.like('%or%')) #запрос на получение, где в name содержится 'or'

#result = db.query(Users).filter(Users.name.in_(['alora'])) #запрос на получение строчек с указанной переменной,
                                                                 #хранящейся в name




