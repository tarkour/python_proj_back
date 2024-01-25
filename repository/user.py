

class UserRepository:

    def __init__(self, session):
        self.session

    @property
    def model(self) -> Password:
        return Password

