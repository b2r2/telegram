import telebot


class Commands():
    def __init__(self, bot, db, path, utils_string):
        self.bot = bot
        self.db = db
        self.utils_string = utils_string

    def handle_start(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('/start', '/help')
        user_markup.row('/channel', '/schedule')
        user_markup.row('/advertising', '/mydata')

        msg = """Hello!"""
        self.bot.send_message(message.from_user.id, msg,
                              reply_markup=user_markup)

    def handle_help(self, message):
        msg = """My options are very limited..."""
        self.bot.send_message(message.from_user.id, msg)

    def handle_advertising(self, message):
        msg = "Give me your advertising message:"
        self.bot.send_message(message.from_user.id, msg)

    def handle_channel(self, message):
        msg = "Please enter the name of the channel (e.g. @yourchannel)"
        self.bot.send_message(message.from_user.id, msg)

    def handle_schedule(self, message):
        msg = "Here you can set up a schedule to release your" + \
            " advertising message in the system.\n" + \
            "Please enter only the hours without minutes" + \
            " (e.g. 01:00 or 23:15,  etc.):"
        self.bot.send_message(message.from_user.id, msg)

    def handle_data(self, message):
        msg = "Your data is in the format (channel name,"\
                "advertising message, schedule)"
        self.bot.send_message(message.from_user.id, msg)

        data = self.db.return_data(message.from_user.id, 'mydata')
        data = self.utils_string.formatting_data(data)
        self.bot.send_message(message.from_user.id, data)
