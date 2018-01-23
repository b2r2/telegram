# -*- coding: utf-8 -*-


import cherrypy
import logging
import setup
import telebot
import webhook
import handler
import utils
from config import TOKEN
from config import IGNORE_TYPES
from config import CONTENT_TYPES


bot = telebot.AsyncTeleBot(TOKEN)
handler = handler.MessageHandler(bot)

webhook_server = webhook.WebhookServer(bot)
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


bot.remove_webhook()
bot.set_webhook(url=setup.WEBHOOK_URL_BASE+setup.WEBHOOK_URL_PATH,
                certificate=open(setup.WEBHOOK_SSL_CERT, 'r'))

access_log = cherrypy.log.access_log
for log_handler in tuple(access_log.handlers):
    access_log.removeHandler(log_handler)

cherrypy.config.update(
    {
        'server.socket_host': setup.WEBHOOK_LISTEN,
        'server.socket_port': setup.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': setup.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': setup.WEBHOOK_SSL_PRIV
    }
)

if __name__ == '__main__':
    cherrypy.quickstart(webhook_server, setup.WEBHOOK_URL_PATH, {'/': {}})
