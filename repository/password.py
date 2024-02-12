from model.password import Password
from sqlalchemy import select

class PasswordRepository:

    def __init__(self, session):
        self.session = session

    @property
    def model(self) -> Password:
        return Password

    def check_password_by_user_id(self, user_id, password):
        vals = self.session.scalars(select(Password).
                             where(
                                Password.user_id == user_id,
                                Password.password == password
                             ).
                             order_by(Password.id.desc())
                             ).first()
        return vals is not None

