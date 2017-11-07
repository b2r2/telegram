import json


class Handler():
    def __init__(self, bot, config, markup):
        self.bot = bot
        self.config = config
        self.markup = markup
        self.user_chat_id = 0

    def start(self, message):
        buttons = self.config.buttons_name
        keyboard = self.markup.create_keyboard(**buttons)
        self.bot.send_message(message.chat.id,
                              self.config.info['start'],
                              reply_markup=keyboard)

    def send_post_about(self, message):
        self.bot.send_message(message.chat.id,
                              self.config.info['about'])

    def send_post_feedback(self, message):
        self.bot.send_message(message.chat.id,
                              self.config.info['feedback'])

    def send_post_advertising(self, message):
        self.bot.send_message(message.chat.id,
                              self.config.info['advertising'])

    def send_post_suggest(self, message):
        self.bot.send_message(message.chat.id,
                              self.config.info['suggest'])

    def send_ignore_post(self, message):
        smiley = u'\U0001F609'
        msg = u'Извините, но я различаю только текст и смайлики ' + smiley
        self.bot.send_message(message.chat.id, msg)

    def send_simple_message(self, message):
        smiley = u'\U0001F609'
        msg = u'Ваше сообщение отправлено!\nСпасибо! ' + smiley
        if message.chat.id == self.config.ADMIN_CHAT_ID:
            pass
        else:
            self.bot.send_message(message.chat.id, msg)

    def forward_message(self, message):
        if message.chat.id != self.config.ADMIN_CHAT_ID:
            self.bot.forward_message(self.config.ADMIN_CHAT_ID,
                                     message.chat.id, message.message_id)

    def send_admin_message(self, message):
        self.bot.send_message(self.user_chat_id, message.text)

    def send_button(self, text, inline_button):
        self.bot.send_message(chat_id=self.config.ADMIN_CHAT_ID,
                              text=text,
                              reply_markup=inline_button)

    def parse_user_message(self, message):
        if message.chat.id != self.config.ADMIN_CHAT_ID:
            self.take_user_message(message)
        if self.user_chat_id and message.chat.id == self.config.ADMIN_CHAT_ID:
            self.answer_admin_message(message)

    def take_user_message(self, message):
        text = 'Сообщение от {}'.format(message.chat.first_name)
        button_name = 'Answer'
        user_name = ' {}'.format(message.chat.first_name)
        data = self.encode_message(message, button_name)
        inline_button = self.markup.create_inline_button(button_name + user_name,
                                                         data)
        self.forward_message(message)
        self.send_button(text, inline_button)

    def answer_admin_message(self, message):
        text = 'Сообщение {} отправлено!'.format(message.chat.first_name)
        button_name = 'Reset'
        data = self.encode_message(message, button_name)
        inline_button = self.markup.create_inline_button(button_name, data)
        self.send_admin_message(message)
        self.send_button(text, inline_button)

    def set_user_chat_id(self, user_chat_id):
        self.user_chat_id = user_chat_id

    def reset_user_chat_id(self):
        self.user_chat_id = 0

    def return_user_chat_id(self):
        return self.user_chat_id

    def encode_message(self, message, button):
        message_data = {
            'name': message.chat.first_name,
            'cid': message.chat.id,
            'action': button
        }
        return json.dumps(message_data)

    def decode_message(self, message_data):
        return json.loads(message_data)

    def send_bot_answer_message(self, call, message_data):
        if message_data['action'] == 'Reset':
            self.reset_user_chat_id()
            message_text = 'Чат с {} сброшен'.format(message_data['name'])
            self.bot.answer_callback_query(callback_query_id=call.id,
                                           show_alert=False,
                                           text=message_text)
        elif message_data['action'] == 'Answer':
            message_text = 'Чат с {} выбран'.format(message_data['name'])
            self.set_user_chat_id(message_data['cid'])
            self.bot.answer_callback_query(callback_query_id=call.id,
                                           show_alert=False,
                                           text=message_text)
