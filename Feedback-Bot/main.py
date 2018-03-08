# -*- coding: utf-8 -*-


import cherrypy
import logging
import telebot
import webhook
import handler
import utils
import config


bot = telebot.AsyncTeleBot(config.TOKEN)
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
                     content_types=config.IGNORE_TYPES)
def sending_error(message):
    handler.send_error(message.chat.id,
                       'Please sending only text, photo or sticker')


@bot.message_handler(func=lambda message: message.chat.type in 'private',
                     content_types=config.CONTENT_TYPES)
def forwarding_message(message):
    handler.forward_message(message)


bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL_BASE+config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

access_log = cherrypy.log.access_log
for log_handler in tuple(access_log.handlers):
    access_log.removeHandler(log_handler)

cherrypy.config.update(
    {
        'server.socket_host': config.WEBHOOK_LISTEN,
        'server.socket_port': config.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
    }
)

if __name__ == '__main__':
    cherrypy.quickstart(webhook_server, config.WEBHOOK_URL_PATH, {'/': {}})
