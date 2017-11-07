#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
from telebot import types
import handler
import config
import markup


bot = telebot.TeleBot(config.TOKEN)
markup = markup.Markup(types)
handler = handler.Handler(bot, config, markup)

ignore_types = config.ignore_types


@bot.message_handler(func=lambda message: message.text == '/start')
def message_start(message):
    handler.start(message)


@bot.message_handler(func=lambda message: message.text == u'О канале')
def message_about(message):
    handler.send_post_about(message)


@bot.message_handler(func=lambda message: message.text == u'Отзывы и предложения')
def message_feedback(message):
    handler.send_post_feedback(message)


@bot.message_handler(func=lambda message: message.text == u'Условия рекламы')
def message_advertising(message):
    handler.send_post_advertising(message)


@bot.message_handler(func=lambda message: message.text == u'Предложить новость')
def message_suggest(message):
    handler.send_post_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def ignore_message(message):
    handler.send_ignore_post(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_message(message):
    handler.send_simple_message(message)
    handler.parse_user_message(message)


@bot.callback_query_handler(func=lambda call: call.data)
def handle_callback(call):
    message_data = handler.decode_message(call.data)
    handler.send_bot_answer_message(call, message_data)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
