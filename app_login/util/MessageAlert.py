
class MessageAlert():
    messages = []

    def __init__(self):
        self.messages = []

    #def __init__(self, message):
    #    self.messages.append(message)

    def add(self, message):
        self.messages.append(message)