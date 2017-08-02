import utils.string as us


class Handler():
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def handle_advertising_message(self, message):
        self.bot.send_message(message.from_user.id,
                              "It is your advertising message:")

        self.db.update_adv_message(message.from_user.id,
                                   message.text,
                                   message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_field(message.from_user.id,
                                                   'advertising'))

        self.bot.send_message(message.from_user.id, "If you see the error,"
                              " try again!")

    def handle_channel_message(self, message):
        self.bot.send_message(message.from_user.id, "It is your channel:")

        self.db.update_channel_message(message.from_user.id,
                                       message.text,
                                       message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_field(message.from_user.id,
                                                   'channel'))
        self.bot.send_message(message.from_user.id, "If you see the error,"
                              " try again!")

    def handle_schedule_message(self, message):
        self.bot.send_message(message.from_user.id, "It's your schedule:")
        self.db.update_schedule_message(message.from_user.id,
                                        us.formatting_schedule(
                                            message.text),
                                        message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_field(message.from_user.id,
                                                   'schedule'))
        self.bot.send_message(message.from_user.id,
                              "If you see the error try again!")
