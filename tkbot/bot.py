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


#########################################
@bot.message_handler(commands=['start'])
def handleStart(message):
    handler.handleStart(message)


@bot.message_handler(commands=['help'])
def handleHelp(message):
    handler.handleHelp(message)


@bot.message_handler(commands=['mydata'])
def handleData(message):
    handler.handleData(message)


@bot.message_handler(commands=['advertising'])
def handleAdvertising(message):
    user_will_send_advertising.add(message.from_user.id)
    handler.handleAdvertising(message)


@bot.message_handler(commands=['channel'])
def handleChannel(message):
    user_will_send_channel.add(message.from_user.id)
    handler.handleChannel(message)


@bot.message_handler(commands=['schedule'])
def handleSchedule(message):
    user_will_send_schedule.add(message.from_user.id)
    handler.handleSchedule(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_advertising)
def handleAdvertisingMessage(message):
    # no photo!
    user_will_send_advertising.remove(message.from_user.id)
    handler.handleAdvertisingMessage(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_channel)
def handleChannelMessage(message):
    user_will_send_channel.remove(message.from_user.id)
    handler.handleChannelMessage(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_schedule)
def handleScheduleMessage(message):
    user_will_send_schedule.remove(message.from_user.id)
    handler.handleScheduleMessage(message)


@bot.message_handler(content_types=['photo'])
def handlePhoto(message):
    handler.handlePhoto(message)


@bot.message_handler(content_types=['sticker'])
def handleSticker(message):
    handler.handleSticker(message)


@bot.message_handler(content_types=['audio'])
def handleAudio(message):
    handler.handleAudio(message)


@bot.message_handler(content_types=['document'])
def handleDocument(message):
    handler.handleDocument(message)


@bot.message_handler(content_types=['video'])
def handleVideo(message):
    handler.handleVideo(message)


@bot.message_handler(content_types=['text'])
def handleText(message):
    handler.handleText(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
