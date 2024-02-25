from datetime import datetime
import pytz
import repository.user
import repository.message
class MessageService():

    def __init__(self, userRepository, messageRepository):
        self.userRepository = userRepository
        self.messageRepository = messageRepository

    def send_message(self,user, message):
        user_model = self.userRepository.model
        user_id = user_model.get_user_id()
        current_time = datetime.now(pytz.timezone('Europe/Moscow'))
        message_data = self.messageRepository.model(user_id, message, current_time)

    def get_messages(self, per_page=100, page=1):

        all_msg_count = DBSession.query(Messages).count()
        if  all_msg_count == 0:
            return render_template('messages.html')
        max_pages_count = all_msg_count // per_page
        if all_msg_count % per_page != 0:
            max_pages_count += 1

        if page_num > max_pages_count: #обработка случая, когда пользователь вводит в адерсную строку страницу,
                                       #превышающую максимальное количество страниц
            return redirect(url_for('messages_pagination', page_num=max_pages_count)) # В РЕДИРЕКТ НАДО ПИСАТЬ НАЗВАНИЕ ФУНКЦИИ, А НЕ ЕНДПОИНТ!!
        if page_num < 1: #обработка случая "0" в адресной строке
            return redirect(url_for('messages_pagination', page_num=1))

        all_msg = DBSession.query(Messages).all()[::-1]
        msg_left = per_page - (all_msg_count % per_page)


        if page_num == max_pages_count: # берем массив сообщений нужного диапазона
            all_messages = all_msg[
                           page_num * per_page - per_page: page_num * per_page - msg_left]
        else:
            all_messages = all_msg[page_num * per_page - per_page: page_num * per_page]

        url = '/messages/page/'
        if page_num == 1:  # создание ссылки на страницу назад
            previuos = url + str(1)
        else:
            previuos = url + str(page_num - 1)

        if page_num == max_pages_count:  # создание ссылки на страницу вперед
            next = url + str(max_pages_count)
        else:
            next = url + str(page_num + 1)