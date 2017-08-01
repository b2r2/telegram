import logging
import utils.string as us


class Log():
    def __init__(self, path):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                                      '# (%(asctime)s)',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        filehandler = logging.FileHandler(path.log)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.ERROR)

        copy_filehandler = logging.FileHandler(path.clog)
        copy_filehandler.setFormatter(formatter)
        copy_filehandler.setLevel(logging.ERROR)

        self.logger.addHandler(console)
        self.logger.addHandler(filehandler)
        self.logger.addHandler(copy_filehandler)

    def error(self, function_name, msg):
        self.logger.exception('Error:  %s. Sending a file(type %s)',
                              function_name, msg)

    def info(self, function_name):
        self.logger.info('%s: success', function_name)


class Handler():
    def __init__(self, bot, db, path):
        self.string = us.String()
        self.log = Log(path)
        self.bot = bot
        self.db = db

    def handle_advertising_message(self, message):
        self.bot.send_message(message.from_user.id,
                              "It is your advertising message:")

        self.db.update_adv_message(message.from_user.id,
                                   message.text,
                                   message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_data(message.from_user.id,
                                                  'advertising'))

        self.bot.send_message(message.from_user.id, "If you see the erorr,"
                              " try again!")

    def handle_channel_message(self, message):
        self.bot.send_message(message.from_user.id, "It is your channel:")

        self.db.update_channel_message(message.from_user.id,
                                       message.text,
                                       message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_data(message.from_user.id,
                                                  'channel'))
        self.bot.send_message(message.from_user.id, "If you see the error,"
                              " try again!")

    def handle_schedule_message(self, message):
        self.bot.send_message(message.from_user.id, "It's your schedule:")
        self.db.update_schedule_message(message.from_user.id,
                                        self.string.formatting_schedule(
                                            message.text),
                                        message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_data(message.from_user.id,
                                                  'schedule'))
        self.bot.send_message(message.from_user.id,
                              "If you see the error try again!")
