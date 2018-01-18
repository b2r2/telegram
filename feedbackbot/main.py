# -*- coding: utf-8 -*-


import logging
import telebot
import handler
import utils
from config import TOKEN, IGNORE_TYPES, ADMIN_CHAT_ID


bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(func=utils.is_command)
def handle_command(message):
    handler.send_command(message)


@bot.message_handler(func=lambda message: True, content_types=IGNORE_TYPES)
def invalid_message(message):
    handler.send_ignore(message)


@bot.message_handler(func=lambda message: message.chat.id != ADMIN_CHAT_ID,
                     content_types=['text', 'photo'])
def receive_message(message):
    handler.send_default_message(message)
    handler.handle_user_message(message)


@bot.message_handler(func=lambda message: message.chat.id == ADMIN_CHAT_ID,
                     content_types=['text'])
def send_message(message):
    handler.handle_admin_message(message)


@bot.callback_query_handler(func=utils.is_data)
def handle_callback(call):
    handler.processing_callback_request(call)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
