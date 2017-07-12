import logging
import telebot


class Log():
    def __init__(self, path_log, path_copy_log):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                                      '# (%(asctime)s)',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        filehandler = logging.FileHandler(path_log)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.ERROR)

        copy_filehandler = logging.FileHandler(path_copy_log)
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
    def __init__(self, bot, chat_id, database, path_log, path_copy_log):
        self.log = Log(path_log, path_copy_log)
        self.chat_id = chat_id
        self.bot = bot
        self.db = database

    def handle_Start(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('/start', '/help')
        user_markup.row('/channel', '/schedule')
        user_markup.row('/advertising', '/mydata')

        msg = """Hello!
        \nYou can send message in channel {0}""".format(self.chat_id)
        self.bot.send_message(message.from_user.id, msg,
                              reply_markup=user_markup)

    def handle_Help(self, message):
        msg = """My options are very limited..."""
        self.bot.send_message(message.from_user.id, msg)

    def handle_Data(self, message):
        msg = "Your data is in the format (user ID, channel name,"\
                "advertising message, schedule)"
        self.bot.send_message(message.from_user.id, msg)

        data = self.db.return_All_Database_User(message.from_user.id)

        for user_data in data[0][1:-1]:
            self.bot.send_message(message.from_user.id, user_data)

    def handle_Advertising(self, message):
        msg = "Give me your advertising message:"
        self.bot.send_message(message.from_user.id, msg)

    def handle_Channel(self, message):
        msg = "Please enter the name of the channel (e.g. @yourchannel)"
        self.bot.send_message(message.from_user.id, msg)

    def handle_Schedule(self, message):
        msg = "Here you can set up a schedule to release your" + \
            " advertising message in the system.\n" + \
            "Please enter only the hours without minutes" + \
            " (e.g. 01:00, 23:15, etc.):"
        self.bot.send_message(message.from_user.id, msg)

    def handle_Advertising_Message(self, message):
        # no photo!
        self.bot.send_message(message.from_user.id, "It is your advertising message:")

        self.db.update_Adv_Message_User(message.from_user.id,
                                        message.text,
                                        message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_Adv_Message_User(message.from_user.id))

        self.bot.send_message(message.from_user.id, "If you see the erorr,"
                              " try again!")
        print(self.db.show_Database())

    def handle_Channel_Message(self, message):
        self.bot.send_message(message.from_user.id, "It is your channel:")

        self.db.update_Channel_User(message.from_user.id,
                                    message.text,
                                    message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_Channel_User(message.from_user.id))
        self.bot.send_message(message.from_user.id, "If you see the error,"
                              " try again!")
        print(self.db.show_Database())

    def handle_Schedule_Message(self, message):
        self.bot.send_message(message.from_user.id, "It's your schedule:")

        self.db.update_Schedule_User(message.from_user.id,
                                     message.text,
                                     message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.return_Schedule_User(message.from_user.id))

        self.bot.send_message(message.from_user.id, "If you see the error try again!")
        print(self.db.show_Database())

    def handle_Photo(self, message):
        try:
            msg_photo = message.photo[0].file_id
            self.bot.send_photo(self.chat_id, msg_photo)
        except Exception as err:
            self.log.error(err, self.handle_Photo.__name__)
        else:
            self.log.info(self.handle_Photo.__name__)

    def handle_Sticker(self, message):
        try:
            msg_sticker = message.sticker.file_id
            self.bot.send_sticker(self.chat_id, msg_sticker)
        except Exception as err:
            self.log.error(err, self.handle_Sticker.__name__)
        else:
            self.log.info(self.handle_Sticker.__name__)

    def handle_Audio(self, message):
        try:
            msg_audio = message.audio.file_id
            self.bot.send_audio(self.chat_id, msg_audio)
        except Exception as err:
            self.log.error(err, self.handle_Audio.__name__)
        else:
            self.log.info(self.handle_Audio.__name__)

    def handle_Document(self, message):
        try:
            msg_document = message.document.file_id
            self.bot.send_document(self.chat_id, msg_document)
        except Exception as err:
            self.log.error(err, self.handle_Document.__name__)
        else:
            self.log.info(self.handle_Document.__name__)

    def handle_Video(self, message):
        try:
            msg_video = message.video.file_id
            self.bot.send_video(self.chat_id, msg_video)
        except Exception as err:
            self.log.error(err, self.handle_Video.__name__)
        else:
            self.log.info(self.handle_Video.__name__)

    def handle_Text(self, message):
        try:
            self.bot.send_message(self.chat_id, message.text)
        except Exception as err:
            self.log.error(err, self.handle_Text)
        else:
            self.log.info(self.handle_Text.__name__)
