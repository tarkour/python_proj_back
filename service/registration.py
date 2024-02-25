from flask import render_template
import os


class RegistrationService():

    def __init__(self, passwordRepository, userRepository):
        self.passwordRepository = passwordRepository
        self.userRepository = userRepository

    def registration(self, username, password, repeat_password):
        user = self.userRepository.check_login_if_exists(username)
        if user == True:
            flash('This login has been taken already!')
            return render_template('registration.html')

        if password != repeat_password:
            flash('Passwords are not the same!')
            return render_template('registration.html')

        return username, password

    def commit_new_user(self, username, password):
        user = self.userRepository.model(username)
        DBSession.add(user)
        DBSession.commit()

        user_id = self.userRepository.get_user_id(username)
        password_data = self.passwordRepository.model(user_id, password, True)
        DBSession.add(password_data)
        DBSession.commit()

        flash('Your registration is successful')

