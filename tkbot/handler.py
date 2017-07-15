import logging
import telebot
import utils.string as us


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
        self.string = us.String()
        self.log = Log(path_log, path_copy_log)
        self.chat_id = chat_id
        self.bot = bot
        self.db = database

    def handleStart(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('/start', '/help')
        user_markup.row('/channel', '/schedule')
        user_markup.row('/advertising', '/mydata')

        msg = """Hello!
        \nYou can send message in channel {0}""".format(self.chat_id)
        self.bot.send_message(message.from_user.id, msg,
                              reply_markup=user_markup)

    def handleHelp(self, message):
        msg = """My options are very limited..."""
        self.bot.send_message(message.from_user.id, msg)

    def handleData(self, message):
        msg = "Your data is in the format (channel name,"\
                "advertising message, schedule)"
        self.bot.send_message(message.from_user.id, msg)

        data = self.db.returnAllMessages(message.from_user.id)
        for user_data in data[0][2:-1]:
            self.bot.send_message(message.from_user.id, user_data)

    def handleAdvertising(self, message):
        msg = "Give me your advertising message:"
        self.bot.send_message(message.from_user.id, msg)

    def handleChannel(self, message):
        msg = "Please enter the name of the channel (e.g. @yourchannel)"
        self.bot.send_message(message.from_user.id, msg)

    def handleSchedule(self, message):
        msg = "Here you can set up a schedule to release your" + \
            " advertising message in the system.\n" + \
            "Please enter only the hours without minutes" + \
            " (e.g. 01:00 or 23:15,  etc.):"
        self.bot.send_message(message.from_user.id, msg)

    def handleAdvertisingMessage(self, message):
        self.bot.send_message(message.from_user.id,
                              "It is your advertising message:")

        self.db.updateAdvMessage(message.from_user.id,
                                 message.text,
                                 message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.returnAdvMessage(message.from_user.id))

        self.bot.send_message(message.from_user.id, "If you see the erorr,"
                              " try again!")
        self.db.show()

    def handleChannelMessage(self, message):
        self.bot.send_message(message.from_user.id, "It is your channel:")

        self.db.updateChannelMessage(message.from_user.id,
                                     message.text,
                                     message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.returnChannelMessage(message.from_user.id))
        self.bot.send_message(message.from_user.id, "If you see the error,"
                              " try again!")
        self.db.show()

    def handleScheduleMessage(self, message):
        self.bot.send_message(message.from_user.id, "It's your schedule:")
        self.db.updateScheduleMessage(message.from_user.id,
                                      self.string.formattingSchedule(message.text),
                                      message.date)

        self.bot.send_message(message.from_user.id,
                              self.db.returnScheduleMessage(message.from_user.id))
        self.bot.send_message(message.from_user.id,
                              "If you see the error try again!")
        self.db.show()

    def handlePhoto(self, message):
        try:
            msg_photo = message.photo[0].file_id
            self.bot.send_photo(self.chat_id, msg_photo)
        except Exception as err:
            self.log.error(err, self.handlePhoto.__name__)
        else:
            self.log.info(self.handlePhoto.__name__)

    def handleSticker(self, message):
        try:
            msg_sticker = message.sticker.file_id
            self.bot.send_sticker(self.chat_id, msg_sticker)
        except Exception as err:
            self.log.error(err, self.handleSticker.__name__)
        else:
            self.log.info(self.handleSticker.__name__)

    def handleAudio(self, message):
        try:
            msg_audio = message.audio.file_id
            self.bot.send_audio(self.chat_id, msg_audio)
        except Exception as err:
            self.log.error(err, self.handleAudio.__name__)
        else:
            self.log.info(self.handleAudio.__name__)

    def handleDocument(self, message):
        try:
            msg_document = message.document.file_id
            self.bot.send_document(self.chat_id, msg_document)
        except Exception as err:
            self.log.error(err, self.handleDocument.__name__)
        else:
            self.log.info(self.handleDocument.__name__)

    def handleVideo(self, message):
        try:
            msg_video = message.video.file_id
            self.bot.send_video(self.chat_id, msg_video)
        except Exception as err:
            self.log.error(err, self.handleVideo.__name__)
        else:
            self.log.info(self.handleVideo.__name__)

    def handleText(self, message):
        try:
            self.bot.send_message(self.chat_id, message.text)
        except Exception as err:
            self.log.error(err, self.handleText)
        else:
            self.log.info(self.handleText.__name__)
