import config
import text
import data
import markup
import sender


class MessageHandler():
    def __init__(self, bot):
        self.bot = bot
        self.sender = sender.SenderMessage(bot)
        self.markup = markup.KeyboardMarkupFactory()
        self.data = data.DataHandler()

    def send_start(self, message):
        keyboard = self.markup.create_keyboard(**config.BUTTON_NAMES)
        self.sender.publish_start(message.chat.id,
                                  keyboard,
                                  config.INFO['start'])

    def send_about(self, message):
        self.sender.publish_command_message(message.chat.id,
                                            config.INFO['about'])

    def send_feedback(self, message):
        self.sender.publish_command_message(message.chat.id,
                                            config.INFO['feedback'])

    def send_advertising(self, message):
        button = self.markup.create_url_inline_button('Перейти',
                                                      config.ADVERTISING_LINK)
        self.sender.publish_url_inline_button(message.chat.id,
                                              config.INFO['advertising'],
                                              button)

    def send_suggest(self, message):
        self.sender.publish_command_message(message.chat.id,
                                            config.INFO['suggest'])

    def send_ignore(self, message):
        self.sender.publish_message(message.chat.id,
                                    text.IGNORE)

    def send_default_message(self, message):
        self.sender.publish_message(message.chat.id,
                                    text.DEFAULT)

    def processing_callback_request(self, call):
        try:
            text = self.data.get_admin_action_button_text()
        except Exception:
            self.sender.publish_message(config.ADMIN_CHAT_ID,
                                        'No user data')
        else:
            self.sender.publish_answer_callback_query(call,
                                                      text)

    def handle_user_message(self, message):
        self.data.set_data([message.chat.id,
                            message.chat.first_name])
        inline_button = self.make_callback_button('Answer')
        self.sender.forward_message(config.ADMIN_CHAT_ID,
                                    message)
        self.send_callback_button(inline_button)

    def handle_admin_message(self, message):
        user_data = self.data.get_data()
        user_name = user_data['user_name']
        if user_name is not None and len(user_name) > 0:
            inline_button = self.make_callback_button('Reset')
            self.sender.publish_message(user_data['cid'],
                                        message.text)
            self.send_callback_button(inline_button)
        else:
            self.sender.publish_message(config.ADMIN_CHAT_ID,
                                        text.MISTAKE)

    def send_callback_button(self, inline_button):
        text = self.data.get_callback_button_text()
        self.sender.publish_callback_inline_button(config.ADMIN_CHAT_ID,
                                                   text,
                                                   inline_button)

    def make_callback_button(self, button_name):
        self.data.set_action(button_name)
        user_data = self.data.get_data()
        button = ' '.join([button_name,
                           user_data['user_name']])
        data = self.data.encode_data()
        return self.markup.create_callback_inline_button(button,
                                                         data)
