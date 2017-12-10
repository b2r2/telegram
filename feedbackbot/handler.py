# -*- coding: utf-8 -*-


import config
import text
import data
import utils


class MessageHandler():
    def __init__(self, bot):
        self.bot = bot
        self.data = data.UserDataHandler()

    def send_start(self, message):
        keyboard = utils.create_keyboard(**config.BUTTON_NAMES)
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.INFO['start'],
                              reply_markup=keyboard)

    def send_about(self, message):
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.INFO['about'])

    def send_feedback(self, message):
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.INFO['feedback'])

    def send_advertising(self, message):
        button = utils.create_url_inline_button(button='Перейти',
                                                url=config.ADVERTISING_LINK)
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.INFO['advertising'],
                              reply_markup=button)

    def send_suggest(self, message):
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.INFO['suggest'])

    def send_ignore(self, message):
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.IGNORE)

    def send_default_message(self, message):
        self.bot.send_message(chat_id=message.chat.id,
                              text=text.DEFAULT)

    def processing_callback_request(self, call):
        try:
            self.data.upgrade_data(data=call)
            alert_text = self.get_admin_action_callback_text()
        except LookupError:
            self.bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                                  text=text.MISTAKE)
        else:
            self.bot.answer_callback_query(callback_query_id=call.id,
                                           text=alert_text,
                                           show_alert=False)
            self.data.is_admin_action()

    def handle_user_message(self, message):
        self.data.set_data(user_data=[message.chat.id,
                                      message.chat.first_name])
        button = self.make_callback_button(button_name='Answer')
        self.bot.forward_message(chat_id=config.ADMIN_CHAT_ID,
                                 from_chat_id=message.chat.id,
                                 message_id=message.message_id)
        self.send_callback_button(inline_button=button)

    def handle_admin_message(self, message):
        user_data = self.data.get_data()
        user_name = user_data['user_name']
        is_user_name = user_name is not None
        if is_user_name and len(user_name) > 0:
            button = self.make_callback_button(button_name='Reset')
            self.bot.send_message(chat_id=user_data['cid'],
                                  text=message.text)
            self.send_callback_button(inline_button=button)
        else:
            self.bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                                  text=text.MISTAKE)

    def send_callback_button(self, inline_button):
        notice_text = self.get_callback_button_text()
        self.bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                              text=notice_text,
                              reply_markup=inline_button)

    def make_callback_button(self, button_name):
        self.data.set_button(button=button_name)
        user_data = self.data.get_data()
        button = ' '.join([button_name,
                           user_data['user_name']])
        return utils.create_callback_inline_button(button=button,
                                                   data=self.data.encode_data())

    def get_admin_action_callback_text(self):
        user_data = self.data.get_data()
        name = user_data['user_name']
        action = user_data['button_name']
        alert_text = {
            'Reset': 'Чат сброшен',
            'Answer': 'Чат c {} выбран'.format(name),
        }
        return alert_text[action]

    def get_callback_button_text(self):
        user_data = self.data.get_data()
        name = user_data['user_name']
        action = user_data['button_name']
        action_to_state = {
            'Answer': 'от {}',
            'Reset': '{} отправлено',
        }
        chat_state = action_to_state[action].format(name)
        notice_text = 'Сообщение {}'.format(chat_state)
        return notice_text
