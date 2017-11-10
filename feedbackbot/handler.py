import json
import markup
import config


class MessageHandler():
    def __init__(self, bot):
        self.bot = bot
        self.markup = markup.KeyboardMarkupFactory()
        self.user_chat_id = 0

    def send_start(self, message):
        buttons = config.BUTTON_NAMES
        keyboard = self.markup.create_keyboard(**buttons)
        self.bot.send_message(message.chat.id,
                              config.INFO['start'],
                              reply_markup=keyboard)

    def send_about(self, message):
            self.bot.send_message(message.chat.id, config.INFO['about'])

    def send_feedback(self, message):
        self.bot.send_message(message.chat.id,
                              config.INFO['feedback'])

    def send_advertising(self, message):
        self.bot.send_message(message.chat.id,
                              config.INFO['advertising'])

    def send_suggest(self, message):
        self.bot.send_message(message.chat.id,
                              config.INFO['suggest'])

    def send_ignore(self, message):
        smiley = u'\U0001F609'
        msg = u'Извините, но я различаю только текст и смайлики ' + smiley
        self.bot.send_message(message.chat.id, msg)

    def send_default_message(self, message):
        smiley = u'\U0001F609'
        msg = u'Ваше сообщение отправлено!\nСпасибо! ' + smiley
        if message.chat.id != config.ADMIN_CHAT_ID:
            self.bot.send_message(message.chat.id, msg)

    def forward_message(self, message):
        if message.chat.id != config.ADMIN_CHAT_ID:
            self.bot.forward_message(config.ADMIN_CHAT_ID,
                                     message.chat.id, message.message_id)

    def send_button(self, text, inline_button):
        self.bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                              text=text,
                              reply_markup=inline_button)

    def parse_user_message(self, message):
        if message.chat.id != config.ADMIN_CHAT_ID:
            self.get_user_message(message)
        if self.user_chat_id and message.chat.id == config.ADMIN_CHAT_ID:
            self.send_admin_message(message)

    def get_user_message(self, message):  # !!!!
        user_name = message.chat.first_name
        button_name = 'Answer'
        button_text = ' '.join([button_name, user_name])
        message_text = 'Сообщение от {}'.format(user_name)
        data = self.encode_message(message, button_name)

        inline_button = self.markup.create_inline_button(button_text, data)
        self.forward_message(message)
        self.send_button(message_text, inline_button)

    def send_admin_message(self, message):
        message_text = 'Сообщение отправлено!'
        button_name = 'Reset'
        data = self.encode_message(message, button_name)

        inline_button = self.markup.create_inline_button(button_name, data)
        self.bot.send_message(self.user_chat_id, message.text)
        self.send_button(message_text, inline_button)

    def set_user_chat_id(self, user_chat_id):
        self.user_chat_id = user_chat_id

    def reset_user_chat_id(self):
        self.user_chat_id = 0

    def encode_message(self, message, button):
        message_data = {
            'user_name': message.chat.first_name,
            'cid': message.chat.id,
            'action': button
        }
        return json.dumps(message_data)

    def decode_message(self, message_data):
        return json.loads(message_data)

    def send_action_inline_button_message(self, call, message_data):
        if message_data['action'] == 'Reset':
            self.reset_user_chat_id()
            message_text = 'Чат с {} сброшен'.format(message_data['user_name'])
            self.bot.answer_callback_query(callback_query_id=call.id,
                                           show_alert=False,
                                           text=message_text)
        elif message_data['action'] == 'Answer':
            message_text = 'Чат с {} выбран'.format(message_data['user_name'])
            self.set_user_chat_id(message_data['cid'])
            self.bot.answer_callback_query(callback_query_id=call.id,
                                           show_alert=False,
                                           text=message_text)
