#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import handler
from config import TOKEN, CONTENT_IGNORE_TYPES
import logging


ignore_types = CONTENT_IGNORE_TYPES

bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)

task = bot.get_me()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def command_start(message):
    handler.send_start(message)


@bot.message_handler(commands=['about'])
@bot.message_handler(func=lambda message: message.text == u'О канале')
def message_about(message):
    handler.send_about(message)


@bot.message_handler(commands=['feedback'])
@bot.message_handler(func=lambda message: message.text == u'Отзывы и предложения')
def message_feedback(message):
    handler.send_feedback(message)


@bot.message_handler(commands=['advertising'])
@bot.message_handler(func=lambda message: message.text == u'Условия рекламы')
def message_advertising(message):
    handler.send_advertising(message)


@bot.message_handler(commands=['suggest'])
@bot.message_handler(func=lambda message: message.text == u'Предложить новость')
def message_suggest(message):
    handler.send_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def invalid_message(message):
    handler.send_ignore(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_message(message):
    handler.send_default_message(message)
    handler.choose_message(message)


@bot.callback_query_handler(func=lambda call: len(call.data) > 0)
def handle_callback(call):
    message_data = handler.decode_message(call.data)
    handler.answer_callback_query(call, message_data)


if __name__ == '__main__':
    result = task.wait()
    bot.polling(none_stop=True, interval=0)
