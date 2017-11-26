import config
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
        keyboard = self.markup.create_keyboard(**config.BUTTON_NAMES)
        self.msg.send_start(message.chat.id,
                            keyboard,
                            config.INFO['start'])

    def send_about(self, message):
        self.msg.send_command_message(message.chat.id,
                                      config.INFO['about'])

    def send_feedback(self, message):
        self.msg.send_command_message(message.chat.id,
                                      config.INFO['feedback'])

    def send_advertising(self, message):
        button = self.markup.create_url_inline_button('Перейти',
                                                      config.ADVERTISING_LINK)
        self.msg.send_url_inline_button(message.chat.id,
                                        config.INFO['advertising'],
                                        button)

    def send_suggest(self, message):
        self.msg.send_command_message(message.chat.id,
                                      config.INFO['suggest'])

    def send_ignore(self, message):
        self.msg.send_user_message(message.chat.id,
                                   text.IGNORE)

    def send_default_message(self, message):
        self.msg.send_user_message(message.chat.id,
                                   text.DEFAULT)

    def answer_callback_query(self, call):
        text = self.support_data.get_text_inline_button()
        self.msg.answer_callback_query(call,
                                       text)

    def handle_user_message(self, message):
        self.support_data.set_data([message.chat.id,
                                    message.chat.first_name])
        inline_button = self.make_callback_button('Answer')
        self.msg.forward_message(config.ADMIN_CHAT_ID,
                                 message)
        self.prepare_callback_button_text(inline_button)

    def handle_admin_message(self, message):
        user_data = self.support_data.get_data()
        if user_data['user_name']:
            inline_button = self.make_callback_button('Reset')
            user_data = self.support_data.get_data()
            self.msg.send_user_message(user_data['cid'],
                                       message.text)
            self.prepare_callback_button_text(inline_button)
        else:
            self.msg.send_user_message(config.ADMIN_CHAT_ID,
                                       text.EMPTY)

    def prepare_callback_button_text(self, button):
        user_data = self.support_data.get_data()
        action = user_data['action']
        user_name = user_data['user_name']
        action_to_state = {
            'Answer': 'от {}',
            'Reset': '{} отправлено',
        }
        chat_state = action_to_state[action].format(user_name)
        text = 'Сообщение {}'.format(chat_state)
        self.msg.send_callback_inline_button(config.ADMIN_CHAT_ID,
                                             text,
                                             button)

    def make_callback_button(self, button_name):
        self.support_data.set_action(button_name)
        user_data = self.support_data.get_data()
        button = ' '.join([button_name,
                           user_data['user_name']])
        data = self.support_data.encode_data()
        return self.markup.create_callback_inline_button(button,
                                                         data)
