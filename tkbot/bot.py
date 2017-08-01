# -*- coding: utf-8 -*-

import telebot
import commands
import settings
import path
import handler
import db
import utils.string


bot = telebot.TeleBot(settings.token)

user_will_send_advertising = set()
user_will_send_channel = set()
user_will_send_schedule = set()

db = db.Database(path)
utils_string = utils.string.String()
handler = handler.Handler(bot, db, path)
commands = commands.Commands(bot, db, path, utils_string)


@bot.message_handler(commands=['start'])
def handle_start(message):
    commands.handle_start(message)


@bot.message_handler(commands=['help'])
def handle_help(message):
    commands.handle_help(message)


@bot.message_handler(commands=['mydata'])
def handle_data(message):
    commands.handle_data(message)


@bot.message_handler(commands=['advertising'])
def handle_advertising(message):
    user_will_send_advertising.add(message.from_user.id)
    commands.handle_advertising(message)


@bot.message_handler(commands=['channel'])
def handle_channel(message):
    user_will_send_channel.add(message.from_user.id)
    commands.handle_channel(message)


@bot.message_handler(commands=['schedule'])
def handle_schedule(message):
    user_will_send_schedule.add(message.from_user.id)
    commands.handle_schedule(message)


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


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
