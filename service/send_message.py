from datetime import datetime
import pytz
class SendMessage():

    def __init__(self, userRepository, messageRepository):
        self.userRepository = userRepository
        self.messageRepository = messageRepository

    def send_message(self,username, message):
        user_id = self.userRepository.get_user_id(username)
        current_time = datetime.now(pytz.timezone('Europe/Moscow'))
        message_data = self.messageRepository.model(user_id, message, current_time)