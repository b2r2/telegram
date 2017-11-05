# -*- coding: utf-8 -*-


import telebot
from telebot import types
import commands
import settings
import markup
import json


bot = telebot.TeleBot(settings.token)
markup = markup.Markup(types)
commands = commands.CommandsHandler(bot, settings, json)

ignore_types = ['audio', 'document', 'photo', 'sticker', 'video',
                'video_note', 'voice', 'location', 'contact']


@bot.message_handler(commands=['start'])
def command_start(message):
    buttons_names = {
        'about': u'О канале',
        'feedback': u'Отзывы и предложения',
        'advertising': u'Условия рекламы',
        'suggest': u'Предложить новость',
    }
    keyboard = markup.return_keyboard(**buttons_names)
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


@bot.message_handler(func=lambda message: message.text == 'О канале')
def handle_about(message):
    commands.handle_about(message)


@bot.message_handler(func=lambda message: message.text == 'Отзывы и предложения')
def handle_feedback(message):
    commands.handle_feedback(message)


@bot.message_handler(func=lambda message: message.text == 'Условия рекламы')
def handle_advertising(message):
    commands.handle_advertising(message)


@bot.message_handler(func=lambda message: message.text == 'Предложить новость')
def handle_suggest(message):
    commands.handle_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    user_chat_id = commands.handle_return_user_cid()
    if user_chat_id:
        text = 'Сообщение отправлено!'
        button = 'Сброс'
        msg_data = commands.handle_serialization_message(message, button)
        inline_button = markup.return_inline_button(button, msg_data)
        commands.handle_admin_message(message, user_chat_id)
        commands.handle_button(text, inline_button)
    else:
        text = 'Новое сообщение от пользователя ' + str(message.chat.id)
        button = 'Ответить'
        msg_data = commands.handle_serialization_message(message, button)
        inline_button = markup.return_inline_button(button, msg_data)
        commands.handle_message(message)
        commands.handle_forward_message(message)
        commands.handle_button(text, inline_button)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def handle_ignore_message(message):
    commands.handle_ignore(message)


@bot.callback_query_handler(lambda call: True)
def handle_callback(call):
    callback = commands.handle_deserialization_message(call.data)
    if callback['action'] == 'Сброс':
        text = 'Чат с пользователем ' + callback['name'] + ' сброшен'
        commands.handle_reset_user_cid()
        commands.handle_action_callback(text)
    elif callback['action'] == 'Ответить':
        text = 'Выбран чат с пользователем ' + callback['name']
        commands.handle_set_user_cid(callback['cid'])
        commands.handle_action_callback(text)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
