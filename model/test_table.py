from . import BaseModel
from sqlalchemy import Column, Integer, String, DateTime


class TestTable(BaseModel):
    __tablename__ = "test_table"

    id = Column('id', Integer, primary_key=True)
    user_id = Column('name', String)
