# -*- coding: utf-8 -*-

import telebot
import settings
import path
import handler
import db


bot = telebot.TeleBot(settings.token)

chat_id = settings.chat_id

user_will_send_advertising = set()
user_will_send_channel = set()
user_will_send_schedule = set()

db = db.Database(path.db, path.log, path.copy_log)
handler = handler.Handler(bot, chat_id, db, path.log, path.copy_log)


@bot.message_handler(commands=['start'])
def handle_start(message):
    handler.handle_start(message)


@bot.message_handler(commands=['help'])
def handle_help(message):
    handler.handle_help(message)


@bot.message_handler(commands=['mydata'])
def handle_data(message):
    handler.handle_data(message)


@bot.message_handler(commands=['advertising'])
def handle_advertising(message):
    user_will_send_advertising.add(message.from_user.id)
    handler.handle_advertising(message)


@bot.message_handler(commands=['channel'])
def handle_channel(message):
    user_will_send_channel.add(message.from_user.id)
    handler.handle_channel(message)


@bot.message_handler(commands=['schedule'])
def handle_schedule(message):
    user_will_send_schedule.add(message.from_user.id)
    handler.handle_schedule(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_advertising)
def handle_advertising_message(message):
    # no photo!
    user_will_send_advertising.remove(message.from_user.id)
    handler.handle_advertising_message(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_channel)
def handle_channel_message(message):
    user_will_send_channel.remove(message.from_user.id)
    handler.handle_channel_message(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_schedule)
def handle_schedule_message(message):
    user_will_send_schedule.remove(message.from_user.id)
    handler.handle_schedule_message(message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    handler.handle_photo(message)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    handler.handle_sticker(message)


@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    handler.handle_audio(message)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    handler.handle_document(message)


@bot.message_handler(content_types=['video'])
def handle_video(message):
    handler.handle_video(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    handler.handle_text(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
