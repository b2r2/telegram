import markup
from config import ADMIN_CHAT_ID
import utils


class MessageHandler():
    def __init__(self, bot):
        self.bot = bot
        self.markup = markup.KeyboardMarkupFactory()
        self.support_data = utils.SupportData()

    def send_ignore(self, message):
        smiley = u'\U0001F609'
        msg = u'Извините, но я различаю только текст и смайлики ' + smiley
        self.bot.send_message(message.chat.id, msg)

    def send_default_message(self, message):
        smiley = u'\U0001F609'
        msg = u'Ваше сообщение отправлено!\nСпасибо! ' + smiley
        is_admin = message.chat.id == ADMIN_CHAT_ID
        if not is_admin:
            self.bot.send_message(message.chat.id, msg)

    def send_button(self, text, inline_button):
        self.bot.send_message(chat_id=ADMIN_CHAT_ID,
                              text=text,
                              reply_markup=inline_button)

    def forward_message(self, message):
        self.bot.forward_message(ADMIN_CHAT_ID,
                                 message.chat.id, message.message_id)

    def send_admin_message(self, message):
        message_text = 'Сообщение отправлено!'
        button_name = 'Reset'
        inline_button = self.markup.create_inline_button(message, button_name)
        message_data = self.support_data.get_data()
        chat_id = message_data['cid']

        self.send_button(message_text, inline_button)
        self.bot.send_message(chat_id, message.text)

    def get_user_message(self, message):
        user_name = message.chat.first_name
        button_name = 'Answer'
        button_text = ' '.join([button_name, user_name])
        message_text = 'Сообщение от {}'.format(user_name)
        data = self.support_data.encode_data(message, button_name)

        inline_button = self.markup.create_inline_button(button_text, data)
        self.send_button(message_text, inline_button)
        self.forward_message(message)

    def answer_callback_query(self, call):
        text = self.support_data.get_text_inline_button()
        self.bot.answer_callback_query(callback_query_id=call.id,
                                       show_alert=False,
                                       text=text)
