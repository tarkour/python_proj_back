from repository.password import PasswordRepository
from repository.user import UserRepository
from model import User
from typing import Optional

class AuthorizationService():
    def __init__(self, password_repository: PasswordRepository, user_repository: UserRepository):
        self.passwordRepository = password_repository
        self.userRepository = user_repository

    def authorize(self, login, password) -> Optional[User]:

        user = self.userRepository.get_user_by_login(login)

        if user is None:
            return None

        if self.passwordRepository.check_password_by_user_id(user.id, password):
            return user

        return None

