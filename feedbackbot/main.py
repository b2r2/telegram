#!/usr/bin/env python
# -*- coding: utf-8 -*-


import telebot
from telebot import types
import commands
import config
import markup
import webhook
import logging
import cherrypy


bot = telebot.TeleBot(config.TOKEN)
webhook_server = webhook.WebhookServer(bot, types)
markup = markup.Markup(types)
commands = commands.CommandsHandler(bot, config)

ignore_types = ['audio', 'document', 'photo', 'sticker', 'video',
                'video_note', 'voice', 'location', 'contact']


WEBHOOK_HOST = config.IP
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'

WEBHOOK_URL_BASE = 'https://%s:%s' % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = '/%s/' % (config.TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def command_start(message):
    buttons = {
        'about': u'О канале',
        'feedback': u'Отзывы и предложения',
        'advertising': u'Условия рекламы',
        'suggest': u'Предложить новость',
    }
    keyboard = markup.return_keyboard(**buttons)
    commands.handle_start(message, keyboard)


@bot.message_handler(commands=['about'])
def command_about(message):
    commands.handle_about(message)


@bot.message_handler(commands=['feedback'])
def command_feedback(message):
    commands.handle_feedback(message)


@bot.message_handler(commands=['advertising'])
def command_advertising(message):
    commands.handle_advertising(message)


@bot.message_handler(commands=['suggest'])
def command_suggest(message):
    commands.handle_suggest(message)


@bot.message_handler(func=lambda message: message.text == u'О канале')
def handle_about(message):
    commands.handle_about(message)


@bot.message_handler(func=lambda message: message.text == u'Отзывы и предложения')
def handle_feedback(message):
    commands.handle_feedback(message)


@bot.message_handler(func=lambda message: message.text == u'Условия рекламы')
def handle_advertising(message):
    commands.handle_advertising(message)


@bot.message_handler(func=lambda message: message.text == u'Предложить новость')
def handle_suggest(message):
    commands.handle_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def handle_ignore_message(message):
    commands.handle_ignore(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    user_chat_id = commands.handle_return_user_cid()

    commands.handle_message(message)

    if message.chat.id != config.ADMIN_CHAT_ID:
        text = u'Сообщение от ' + message.chat.first_name
        button = 'Answer'
        user_name = message.chat.first_name
        msg_data = commands.handle_serialization_message(message, button)
        inline_button = markup.return_inline_button(button + ' ' + user_name,
                                                    msg_data)

        commands.handle_forward_message(message)

        commands.handle_button(text, inline_button)

    if user_chat_id and message.chat.id == config.ADMIN_CHAT_ID:
        text = u'Сообщение отправлено!'
        button = 'Reset'
        msg_data = commands.handle_serialization_message(message, button)
        inline_button = markup.return_inline_button(button, msg_data)

        commands.handle_admin_message(user_chat_id, message)
        commands.handle_button(text, inline_button)


@bot.callback_query_handler(func=lambda call: call.data)
def handle_callback(call):
    callback = commands.handle_deserialization_message(call.data)
    if callback['action'] == 'Reset':
        text = u'Чат с ' + callback['name'] + u' сброшен'
        commands.handle_reset_user_cid()
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=False, text=text)
    elif callback['action'] == 'Answer':
        text = u'Пользователь ' + callback['name'] + u' выбран'
        commands.handle_set_user_cid(callback['cid'])
        bot.answer_callback_query(callback_query_id=call.id,
                                  show_alert=False, text=text)


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
