from repository.password import PasswordRepository
from repository.user import UserRepository

class AuthorizationService():
    def __init__(self, passwordRepository, userRepository):
        self.passwordRepository = passwordRepository
        self.userRepository = userRepository

    def authorize(self, login, password):
        user = self.userRepository.get_user_by_login(login)

        if user == None:
            return None

        if self.passwordRepository.check_password_by_user_id(user.id, password):
            return user

        return None

