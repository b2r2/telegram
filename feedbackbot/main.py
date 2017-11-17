#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import handler
from config import TOKEN, CONTENT_IGNORE_TYPES, ADMIN_CHAT_ID
import logging
import commands


ignore_types = CONTENT_IGNORE_TYPES

bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)
command = commands.CommandHandler(bot)


task = bot.get_me()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def command_start(message):
    command.send_start(message)


@bot.message_handler(commands=['about'])
@bot.message_handler(func=lambda message: message.text == u'О канале')
def command_about(message):
    command.send_about(message)


@bot.message_handler(commands=['feedback'])
@bot.message_handler(func=lambda message: message.text == u'Отзывы и предложения')
def command_feedback(message):
    command.send_feedback(message)


@bot.message_handler(commands=['advertising'])
@bot.message_handler(func=lambda message: message.text == u'Условия рекламы')
def command_advertising(message):
    command.send_advertising(message)


@bot.message_handler(commands=['suggest'])
@bot.message_handler(func=lambda message: message.text == u'Предложить новость')
def command_suggest(message):
    command.send_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def invalid_message(message):
    handler.send_ignore(message)


@bot.message_handler(func=lambda message: message.chat.id != ADMIN_CHAT_ID,
                     content_types=['text'])
def receive_message(message):
    handler.send_default_message(message)
    handler.get_user_message(message)


@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID,
                     content_types=['text'])
def send_message(message):
    handler.send_admin_message(message)


@bot.callback_query_handler(func=lambda call: len(call.data) > 0)
def handle_callback(call):
    handler.answer_callback_query(call)


if __name__ == '__main__':
    result = task.wait()
    bot.polling(none_stop=True, interval=0)
