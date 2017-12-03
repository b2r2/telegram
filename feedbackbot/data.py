# -*- coding: utf-8 -*-


import json


class UserDataHandler():
    def __init__(self):
        self.data = dict.fromkeys(['cid', 'user_name', 'button_name'])

    def encode_data(self):
        return json.dumps(self.data)

    @staticmethod
    def decode_data(call):
        return json.loads(call.data)

    def set_data(self, user_data):
        self.data = {
            'cid': user_data[0],
            'user_name': user_data[1],
        }

    def set_button(self, button):
        """ append 'button name' in self.data """
        self.data.update({'button_name': button})

    def get_data(self):
        return self.data

    def upgrade_data(self, user_data):
        self.data = self.decode_data(user_data)

    def check_admin_action(self):
        if self.data['button_name'] in 'Reset':
            self.clear_data()

    def clear_data(self):
        self.data.clear()
