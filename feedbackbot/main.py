#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import handler
from config import TOKEN, IGNORE_TYPES


bot = telebot.TeleBot(TOKEN)
handler = handler.MessageHandler(bot)

ignore_types = IGNORE_TYPES


@bot.message_handler(func=lambda message: message.text == '/start')
def message_start(message):
    handler.send_start(message)


@bot.message_handler(func=lambda message: message.text == u'О канале')
def message_about(message):
    handler.send_about(message)


@bot.message_handler(func=lambda message: message.text == u'Отзывы и предложения')
def message_feedback(message):
    handler.send_feedback(message)


@bot.message_handler(func=lambda message: message.text == u'Условия рекламы')
def message_advertising(message):
    handler.send_advertising(message)


@bot.message_handler(func=lambda message: message.text == u'Предложить новость')
def message_suggest(message):
    handler.send_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def invalid_message(message):
    handler.ignore(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_message(message):
    handler.send_default_message(message)
    handler.parse_user_message(message)


@bot.callback_query_handler(func=lambda call: len(call.data) > 0)
def handle_callback(call):
    message_data = handler.decode_message(call.data)
    handler.send_action_inline_button_message(call, message_data)


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True, interval=0)
