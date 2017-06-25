# -*- coding: utf-8 -*-

import telebot
import settings
import utils.db


#########################################################################
# LOG CONFIG ############################################################
#########################################################################

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                              '# (%(asctime)s)',
                              datefmt='%Y-%m-%d %H:%M:%S')

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

filehandler = logging.FileHandler(settings.logs_path)
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)

copy_filehandler = logging.FileHandler(settings.copy_logs_path)
copy_filehandler.setFormatter(formatter)
copy_filehandler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(filehandler)
logger.addHandler(copy_filehandler)

#########################################################################
#  FUNCTIONS ############################################################
#########################################################################


def logErr(function_name, msg):
    logger.exception('Error:  %s. Sending a file(type %s)',
                     function_name, msg)


def logInfo(function_name):
    logger.info('%s: success', function_name)

##########################################################################

bot = telebot.TeleBot(settings.token)

chat_id = settings.chat_id

user_will_send_advertising = set()
emit_advertising_content = {}
db = utils.db.Database()


@bot.message_handler(commands=['advertising'])
def handleAdvertising(message):
    user_will_send_advertising.add(message.from_user.id)
    help_msg = """Give me your advertising message (e.g. @name_channel)
    \nPlease write an advertising post:"""
    bot.send_message(message.from_user.id, help_msg)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_advertising)
def handleAdvertisingMessage(message):
    user_will_send_advertising.remove(message.from_user.id)
    emit_advertising_content[message.from_user.id] = message.text

    bot.send_message(message.from_user.id, "It is your advertising message:")
    bot.send_message(message.from_user.id,
                     emit_advertising_content[message.from_user.id])
    bot.send_message(message.from_user.id, "If wrong try again.")

    db.replaceMessage(message.from_user.id,
                      message.text,
                      message.date)
    db.read()


@bot.message_handler(commands=['start'])
def handleStart(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/help')
    user_markup.row('/advertising')

    help_msg = """Hello!
    \nYou can send message in channel {0}""".format(chat_id)
    bot.send_message(message.from_user.id, help_msg,
                     reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handleHelp(message):
    help_msg = """My options are very limited..."""
    bot.send_message(message.from_user.id, help_msg)


@bot.message_handler(content_types=['photo'])
def handlePhoto(message):
    try:
        msg_photo = message.photo[0].file_id
        bot.send_photo(chat_id, msg_photo)
    except Exception as err:
        logErr(err, handlePhoto.__name__)
    else:
        logInfo(handlePhoto.__name__)


@bot.message_handler(content_types=['sticker'])
def handleSticker(message):
    try:
        msg_sticker = message.sticker.file_id
        bot.send_sticker(chat_id, msg_sticker)
    except Exception as err:
        logErr(err, handleSticker.__name__)
    else:
        logInfo(handleSticker.__name__)


@bot.message_handler(content_types=['audio'])
def handleAudio(message):
    try:
        msg_audio = message.audio.file_id
        bot.send_audio(chat_id, msg_audio)
    except Exception as err:
        logErr(err, handleAudio.__name__)
    else:
        logInfo(handleAudio.__name__)


@bot.message_handler(content_types=['document'])
def handleDocument(message):
    try:
        msg_document = message.document.file_id
        bot.send_document(chat_id, msg_document)
    except Exception as err:
        logErr(err, handleDocument.__name__)
    else:
        logInfo(handleDocument.__name__)


@bot.message_handler(content_types=['video'])
def handleVideo(message):
    try:
        msg_video = message.video.file_id
        bot.send_video(chat_id, msg_video)
    except Exception as err:
        logErr(err, handleVideo.__name__)
    else:
        logInfo(handleVideo.__name__)


@bot.message_handler(content_types=['text'])
def handleText(message):
    try:
        bot.send_message(chat_id, message.text)
    except Exception as err:
        logErr(err, handleText)
    else:
        logInfo(handleText.__name__)


# @bot.message_handler(regexp=".*")
# def handleMessage(message):
#     print(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
