# -*- coding: utf-8 -*-


import logging
import telebot
import handler
import utils
from config import TOKEN
from config import IGNORE_TYPES
from config import CONTENT_TYPES


bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(func=utils.is_command)
def sending_command(message):
    handler.send_command(message)


@bot.message_handler(func=lambda message: message.chat.type in 'supergroup',
                     content_types=['text', 'photo', 'sticker'])
def sending_message(message):
    handler.sending(message)


@bot.message_handler(func=lambda message: message.chat.type in 'supergroup',
                     content_types=IGNORE_TYPES)
def sending_error(message):
    handler.send_error(message.chat.id,
                       'Please sending only text, photo or sticker')


@bot.message_handler(func=lambda message: message.chat.type in 'private',
                     content_types=CONTENT_TYPES)
def forwarding_message(message):
    handler.forward_message(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
