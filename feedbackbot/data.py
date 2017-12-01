import json


class UserDataHandler():
    def __init__(self):
        self.data = dict.fromkeys(['cid', 'user_name', 'action'])

    def encode_data(self):
        return json.dumps(self.data)

    def decode_data(self, call):
        return json.loads(call.data)

    def set_data(self, user_data):
        self.data = {
            'cid': user_data[0],
            'user_name': user_data[1],
        }

    def set_action(self, action):
        self.data.update({'action': action})

    def get_data(self):
        return self.data

    def get_admin_action_button_text(self, call):
        user_data = self.decode_data(call)
        self.data = user_data
        name = user_data['user_name']
        action = user_data['action']
        text = {
            'Reset': 'Чат сброшен',
            'Answer': 'Чат c {} выбран'.format(name),
        }
        if action == 'Reset':
            self.clear_data()
        return text[action]

    def clear_data(self):
        self.data.clear()

    def get_callback_button_text(self):
        action = self.data['action']
        user_name = self.data['user_name']
        action_to_state = {
            'Answer': 'от {}',
            'Reset': '{} отправлено',
        }
        chat_state = action_to_state[action].format(user_name)
        text = 'Сообщение {}'.format(chat_state)
        return text
