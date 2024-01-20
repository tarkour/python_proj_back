from . import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey


class Message(BaseModel):
    __tablename__ = 'messages'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    body = Column('messages', String)
    created_at = Column('date', DateTime(timezone=True))

    def __init__(self, user_id, body, created_at):
        self.user_id = user_id
        self.body = body
        self.created_at = created_at

    def __repr__(self):
        return f'(id: {self.id}, user_id: {self.user_id} body: {self.body}, created_at: {self.created_at})'

    def get_user_id(self):
        return self.user_id
