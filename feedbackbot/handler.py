from config import ADMIN_CHAT_ID, BUTTON_NAMES, INFO
import text
import utils
import markup
import message


class Handler():
    def __init__(self, bot):
        self.bot = bot
        self.msg = message.Message(bot)
        self.markup = markup.KeyboardMarkupFactory()
        self.support_data = utils.SupportData()

    def send_start(self, message):
        keyboard = self.markup.create_keyboard(**BUTTON_NAMES)
        self.msg.send_start(message.chat.id, keyboard, INFO)

    def send_about(self, message):
        self.msg.send_command_message(message, INFO['about'])

    def send_feedback(self, message):
        self.msg.send_command_message(message, INFO['feedback'])

    def send_advertising(self, message):
        self.msg.send_command_message(message, INFO['advertising'])

    def send_suggest(self, message):
        self.msg.send_command_message(message, INFO['suggest'])

    def send_ignore(self, message):
        self.msg.send_user_message(message.chat.id, text.IGNORE)

    def send_default_message(self, message):
        self.msg.send_user_message(message.chat.id, text.DEFAULT)

    def answer_callback_query(self, call):
        text = self.support_data.get_text_inline_button()
        self.bot.answer_callback_query(callback_query_id=call.id,
                                       show_alert=False,
                                       text=text)

    def handle_user_message(self, message):
        self.support_data.set_data([message.chat.id, message.chat.first_name])
        inline_button = self.make_button('Answer')
        self.msg.forward_message(message, ADMIN_CHAT_ID)
        self.send_button(message.chat.first_name, inline_button)

    def handle_admin_message(self, message):
        data = self.support_data.get_data()
        if data['user_name']:
            inline_button = self.make_button('Reset')
            user_data = self.support_data.get_data()
            self.msg.send_user_message(user_data['cid'], message.text)
            self.send_button(user_data['user_name'], inline_button)
        else:
            self.msg.send_user_message(ADMIN_CHAT_ID, text.EMPTY)

    def make_button(self, button_name):
        self.support_data.set_action(button_name)
        user_data = self.support_data.get_data()
        button = ' '.join([button_name, user_data['user_name']])
        data = self.support_data.encode_data()
        return self.markup.create_inline_button(button, data)

    def send_button(self, user_name, button):
        user_data = self.support_data.get_data()
        action = user_data['action']
        user_name = user_data['user_name']
        action_to_state = {
            'Answer': 'от {}',
            'Reset': '{} отправлено',
        }
        chat_state = action_to_state[action].format(user_name)
        text = 'Сообщение {}'.format(chat_state)
        self.msg.send_inline_button(ADMIN_CHAT_ID, text, button)
