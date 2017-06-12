# -*- coding: utf-8 -*-

import telebot
import settings


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


def log_err(msg, chat_id):
    logger.exception('Error sending a file(type %s) to the channel: %s',
                     msg.upper(), chat_id)


def log_info(msg):
    logger.info('Start handler: %-10s' % msg.upper())
    logger.info('Successful: %-13s' % msg.upper())

##########################################################################

bot = telebot.TeleBot(settings.token)

chat_id = settings.chat_id

user_will_send_advertising = set()


def handle_advertising_message(message):
    help_msg = """Get me your advertising message (e.g. @name)
    \nPlease write an advertising post:"""
    bot.send_message(message.from_user.id, help_msg)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if message.text == '/advertising':
        user_will_send_advertising.add(user_id)
    elif user_id in user_will_send_advertising:
        handle_advertising_message(message)
        user_will_send_advertising.remove(user_id)
    else:
        @bot.message_handler(commands=['start'])
        def handle_start(message):
            user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
            user_markup.row('/start', '/help')
            user_markup.row('/advertising')

            help_msg = """Hello!
            \nYou can send message in channel {0}""".format(chat_id)
            bot.send_message(message.from_user.id, help_msg,
                             reply_markup=user_markup)

        @bot.message_handler(commands=['help'])
        def handle_help(message):
            help_msg = """My options are very limited..."""
            bot.send_message(message.from_user.id, help_msg)

        @bot.message_handler(content_types=['photo'])
        def handle_photo(message):
            try:
                msg_photo = message.photo[0].file_id
                bot.send_photo(chat_id, msg_photo)
                log_info('photo')
            except Exception:
                log_err('photo', chat_id)

        @bot.message_handler(content_types=['sticker'])
        def handle_sticker(message):
            try:
                msg_sticker = message.sticker.file_id
                bot.send_sticker(chat_id, msg_sticker)
                log_info('stiker')
            except Exception:
                log_err('stiker', chat_id)

        @bot.message_handler(content_types=['audio'])
        def handle_audio(message):
            try:
                msg_audio = message.audio.file_id
                bot.send_audio(chat_id, msg_audio)
                log_info('audio')
            except Exception:
                log_err('audio', chat_id)

        @bot.message_handler(content_types=['document'])
        def handle_document(message):
            try:
                msg_document = message.document.file_id
                bot.send_document(chat_id, msg_document)
                log_info('document')
            except Exception:
                log_err('document', chat_id)

        @bot.message_handler(content_types=['video'])
        def handle_video(message):
            try:
                msg_video = message.video.file_id
                bot.send_video(chat_id, msg_video)
                log_info('video')
            except Exception:
                log_err('video', chat_id)

        @bot.message_handler(content_types=['text'])
        def handle_text(message):
            bot.send_message(chat_id, message.text)
            log_info('text')


# @bot.message_handler(regexp=".*")
# def handle_message(message):
#     print(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
