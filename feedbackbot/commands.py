import markup
import config


class CommandHandler(object):
    def __init__(self, bot):
        self.bot = bot
        self.markup = markup.KeyboardMarkupFactory()

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
