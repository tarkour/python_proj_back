from . import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.schema import ForeignKey


class Password(BaseModel):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
    password = Column('value', String)
    is_active = Column('is_active', Boolean)

    def __init__(self, user_id, password, is_active):
        self.user_id = user_id
        self.password = password
        self.is_active = is_active

    def __repr__(self):
        return f'({self.user_id} {self.password})'

    def get_user_id(self):
        return self.user_id

    def get_pass(self):
        return self.password

    def is_active(self):
        return self.is_active