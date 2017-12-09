# -*- coding: utf-8 -*-


import logging
import telebot
import handler
import utils
from config import TOKEN, IGNORE_TYPES, ADMIN_CHAT_ID


bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def command_start(message):
    handler.send_start(message)


@bot.message_handler(commands=['about'])
@bot.message_handler(func=lambda message: message.text == u'О канале')
def command_about(message):
    handler.send_about(message)


@bot.message_handler(commands=['feedback'])
@bot.message_handler(func=lambda message: message.text == u'Отзывы и предложения')
def command_feedback(message):
    handler.send_feedback(message)


@bot.message_handler(commands=['advertising'])
@bot.message_handler(func=lambda message: message.text == u'Условия рекламы')
def command_advertising(message):
    handler.send_advertising(message)


@bot.message_handler(commands=['suggest'])
@bot.message_handler(func=lambda message: message.text == u'Предложить новость')
def command_suggest(message):
    handler.send_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=IGNORE_TYPES)
def invalid_message(message):
    handler.send_ignore(message)


@bot.message_handler(func=lambda message: message.chat.id != ADMIN_CHAT_ID,
                     content_types=['text'])
def receive_message(message):
    handler.send_default_message(message)
    handler.handle_user_message(message)


@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID,
                     content_types=['text'])
def send_message(message):
    handler.handle_admin_message(message)


@bot.callback_query_handler(func=utils.is_check_data)
def handle_callback(call):
    handler.processing_callback_request(call)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
