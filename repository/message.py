from model.message import Message
from typing import List

class MessageRepository():
    def __init__(self, session):
        self.session = session

    @property
    def model(self) -> Message:
        return Message

    def get_messages(self) -> List[Message]:
        pass