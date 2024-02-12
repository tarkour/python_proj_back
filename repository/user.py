from model.user import User
from sqlalchemy import select

class UserRepository:

    def __init__(self, session):
        self.session

    @property
    def model(self) -> User:
        return User

    def check_login_if_exists(self, login):
        value = self.query(Users).filter(Users.name == login).all()
        return False if value == [] else True

    def get_user_by_login(self, login):
        value = self.query(Users).filter(Users.name == login).first()
        return value if value != [] else None

    def get_user_id(self, login):
        return login.get_id()