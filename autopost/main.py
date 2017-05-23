# -*- coding: utf-8 -*-


import telebot
import settings


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
    bot.send_message(message.from_user.id, "Мои возможности "
                     "весьма ограниченны...\n"
                     "Я умею отправлять фото, смайлики, стикеры и текст...")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    smallest_photo = message.photo[0].file_id
    bot.send_photo(chat_id, smallest_photo)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    sticker = message.sticker.file_id
    bot.send_sticker(chat_id, sticker)


@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    audio = message.audio.file_id
    bot.send_audio(chat_id, audio)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(chat_id, message.text)


# bot.polling(none_stop=True, interval=0)
