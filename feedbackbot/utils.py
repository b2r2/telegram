import json


class SupportData():
    def __init__(self):
        self.data = {}

    def encode_data(self, message, button):
        self.data = {
            'cid': message.chat.id,
            'action': button,
            'user_name': message.chat.first_name,
        }
        return json.dumps(self.data)

    def get_data(self):
        return self.data

    def get_formatted_text(self):
        user_name = self.data['user_name']
        action = self.data['action']
        text = {
            'Reset': 'Чат сброшен',
            'Answer': 'Чат c {} выбран'.format(user_name),
        }
        if action == 'Reset':
            self.data = {}
        return text[action]

    def get_text_inline_button(self):
        return self.get_formatted_text()
