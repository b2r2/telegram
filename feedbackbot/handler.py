import markup
import config
import utils


class MessageHandler():
    def __init__(self, bot):
        self.bot = bot
        self.markup = markup.KeyboardMarkupFactory()
        self.user_chat_id = 0

    def send_ignore(self, message):
        smiley = u'\U0001F609'
        msg = u'Извините, но я различаю только текст и смайлики ' + smiley
        self.bot.send_message(message.chat.id, msg)

    def send_default_message(self, message):
        smiley = u'\U0001F609'
        msg = u'Ваше сообщение отправлено!\nСпасибо! ' + smiley
        if message.chat.id != config.ADMIN_CHAT_ID:
            self.bot.send_message(message.chat.id, msg)

    def send_button(self, text, inline_button):
        self.bot.send_message(chat_id=config.ADMIN_CHAT_ID,
                              text=text,
                              reply_markup=inline_button)

    def forward_message(self, message):
        if message.chat.id != config.ADMIN_CHAT_ID:
            self.bot.forward_message(config.ADMIN_CHAT_ID,
                                     message.chat.id, message.message_id)

    def choose_message(self, message):
        is_admin = message.chat.id == config.ADMIN_CHAT_ID
        if not is_admin:
            self.get_user_message(message)
        elif self.user_chat_id > 0:
            self.send_admin_message(message)

    def send_admin_message(self, message):
        message_text = 'Сообщение отправлено!'
        button_name = 'Reset'
        data = utils.encode_message(message, button_name)

        inline_button = self.markup.create_inline_button(button_name, data)
        self.send_button(message_text, inline_button)
        self.bot.send_message(self.user_chat_id, message.text)

    def get_user_message(self, message):
        user_name = message.chat.first_name
        button_name = 'Answer'
        button_text = ' '.join([button_name, user_name])
        message_text = 'Сообщение от {}'.format(user_name)
        data = utils.encode_message(message, button_name)

        inline_button = self.markup.create_inline_button(button_text, data)
        self.send_button(message_text, inline_button)
        self.forward_message(message)

    def answer_callback_query(self, call, message_data):
        message_text = self.parse_action_inline_button(call, message_data)
        self.bot.answer_callback_query(callback_query_id=call.id,
                                       show_alert=False,
                                       text=message_text)

    def parse_action_inline_button(self, call, message_data):
        message_text = utils.get_formatted_text(message_data)
        action = message_data['action']

        if action == 'Reset':
            self.reset_user_chat_id()
        elif action == 'Answer':
            self.set_user_chat_id(message_data['cid'])

        return message_text

    def set_user_chat_id(self, user_chat_id):
        self.user_chat_id = user_chat_id

    def reset_user_chat_id(self):
        self.user_chat_id = 0
