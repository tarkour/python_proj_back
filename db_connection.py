from sqlalchemy import create_engine
from model import BaseModel
from sqlalchemy.orm import sessionmaker


db_engine = create_engine('postgresql+psycopg2://root:111@localhost:5432/test_store', echo=True)
BaseModel.metadata.create_all(bind=db_engine)

db_session_maker = sessionmaker(bind=db_engine)
DBSession = db_session_maker()
