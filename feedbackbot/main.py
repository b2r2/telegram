#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import webhook
import handler
import logging
import cherrypy
from config import TOKEN, CONTENT_IGNORE_TYPES, ADMIN_CHAT_ID, \
    WEBHOOK_PORT, WEBHOOK_LISTEN, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV,\
    WEBHOOK_URL_BASE, WEBHOOK_URL_PATH


bot = telebot.AsyncTeleBot(TOKEN)
webhook_server = webhook.WebhookServer(bot)
handler = handler.Handler(bot)


task = bot.get_me()

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


@bot.message_handler(func=lambda message: True, content_types=CONTENT_IGNORE_TYPES)
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


@bot.callback_query_handler(func=lambda call: len(call.data) > 0)
def handle_callback(call):
    handler.answer_callback_query(call)


bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

cherrypy.config.update(
    {
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV
    }
)

if __name__ == '__main__':
    cherrypy.quickstart(webhook_server, WEBHOOK_URL_PATH, {'/': {}})
