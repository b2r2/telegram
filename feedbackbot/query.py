class Callback():
    def __init__(self):
        self.user_chat_id = 0

    def set_user_chat_id(self, chat_id):
        self.user_chat_id = int(chat_id)

    def get_user_chat_id(self):
        return self.user_chat_id

    def reset_user_chat_id(self):
        self.user_chat_id = 0
