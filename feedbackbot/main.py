# -*- coding: utf-8 -*-


import logging
import telebot
import handler
import utils
from config import TOKEN


bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


@bot.message_handler(func=utils.is_command)
def sending_command(message):
    handler.send_command(message)


@bot.message_handler(func=lambda message: message.chat.type in 'supergroup')
def sending_message(message):
    handler.send_message(message)


@bot.message_handler(func=lambda message: message.chat.type in 'private')
def forwarding_message(message):
    handler.forward_message(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
