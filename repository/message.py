from model.message import Message

class MessageRepository():
    def __init__(self, session):
        self.session = session

    @property
    def model(self) -> Message:
        return Message

