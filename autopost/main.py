# -*- coding: utf-8 -*-


import telebot
import settings
import log


bot = telebot.TeleBot(settings.token)


chat_id = settings.chat_id


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/help')
    bot.send_message(message.from_user.id, " Добрый день!\n"
                     "Отсюда можно отправлять сообщения в"
                     " канал {0}".format(chat_id),
                     reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_help(message):
    msg_help = """Мои возможсности весьма ограниченны...\n
    Я умею отправлять фото, смайлики, стикеры, текст и видео..."""
    bot.send_message(message.from_user.id, msg_help)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        msg_photo = message.photo[0].file_id
        bot.send_photo(chat_id, msg_photo)
        log.log_info('photo')
    except Exception:
        log.log_err()


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    try:
        msg_sticker = message.sticker.file_id
        bot.send_sticker(chat_id, msg_sticker)
        log.log_info('stiker')
    except Exception:
        log.log_err()


@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    try:
        msg_audio = message.audio.file_id
        bot.send_audio(chat_id, msg_audio)
        log.log_info('audio')
    except Exception:
        log.log_err()


@bot.message_handler(content_types=['document'])
def handle_document(message):
    try:
        msg_document = message.document.file_id
        bot.send_document(chat_id, msg_document)
        log.log_info('document')
    except Exception:
        log.log_err()


@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        msg_video = message.video.file_id
        bot.send_video(chat_id, msg_video)
        log.log_info('video')
    except Exception:
        log.log_err()


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(chat_id, message.text)
    log.log_info('text')


bot.polling(none_stop=True, interval=0)
