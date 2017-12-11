# -*- coding: utf-8 -*-


import json
from config import RESET


class UserDataHandler():
    def __init__(self):
        self.data = dict.fromkeys(['cid', 'usr', 'btn'])

    def encode_data(self):
        return json.dumps(self.data)

    def set_data(self, user_data):
        self.data = {
            'cid': user_data[0],
            'usr': user_data[1],
        }

    def set_button(self, button):
        """ append 'button name' in self.data """
        self.data.update({'btn': button})

    def get_data(self):
        return self.data

    def upgrade_data(self, data):
        self.data = json.loads(data.data)

    def is_admin_action(self):
        return self.data['btn'] == RESET

    def clear_data(self):
        for key in self.data.keys():
            self.data[key] = None
