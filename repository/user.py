from model.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepository:

    def __init__(self, db_session: Session):
        self.session = db_session

    @property
    def model(self) -> User:
        return User

    def check_login_if_exists(self, login):
        value = self.session.query(User).filter(User.name == login).all()
        return False if value == [] else True

    def get_user_by_login(self, login: str):
        return self.session.query(User).filter(User.name == login).first()

    def get_user_by_login__(self, login: str) -> User:
        "select * from user where login='{}'".format(login)
        return login.get_id()
