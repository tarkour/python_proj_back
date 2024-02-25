from datetime import datetime
import pytz
import repository.user
class SendMessage():

    def __init__(self, userRepository, messageRepository):
        self.userRepository = userRepository
        self.messageRepository = messageRepository

    def send_message(self,user, message):
        user_model = self.userRepository.model
        user_id = user_model.get_user_id()
        current_time = datetime.now(pytz.timezone('Europe/Moscow'))
        message_data = self.messageRepository.model(user_id, message, current_time)

    def get_messages(self, per_page=100, page=1):
        pass