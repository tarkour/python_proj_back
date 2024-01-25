from . import BaseModel
from sqlalchemy import Column, Integer, String


class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'({self.id} {self.name})'

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
