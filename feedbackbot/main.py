#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
import webhook
import logging
import cherrypy
import handler
from config import TOKEN, IP, CONTENT_IGNORE_TYPES


ignore_types = CONTENT_IGNORE_TYPES

bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)
webhook_server = webhook.WebhookServer(bot)

task = bot.get_me()

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

WEBHOOK_HOST = IP
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % (TOKEN)


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
