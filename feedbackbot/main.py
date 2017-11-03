# -*- coding: utf-8 -*-


import telebot
from telebot import types
import commands
import settings
import callback as cb
import markup


bot = telebot.TeleBot(settings.token)
markup = markup.Markup(types)
commands = commands.CommandsHandler(bot, settings)
callback = cb.Callback()

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
    keyboard = markup.get_keyboard(**buttons_names)
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
    user_chat_id = callback.get_user_chat_id()
    if user_chat_id:
        text = 'Сообщение ' + message.chat.first_name + ' отправлено!'
        button_name = 'Сброс'
        inline_button = markup.get_inline_button(button_name, button_name)
        commands.handle_admin_message(message, user_chat_id)
        commands.handle_button(message, text, inline_button)
    else:
        text = 'Новое сообщение!'
        button_name = 'Ответить ' + message.chat.first_name
        inline_button = markup.get_inline_button(button_name, message.chat.id)
        commands.handle_message(message)
        commands.handle_forward_message(message)
        commands.handle_button(message, text, inline_button)


@bot.message_handler(func=lambda message: True, content_types=ignore_types)
def handle_ignore_message(message):
    commands.handle_ignore(message)


@bot.callback_query_handler(lambda call: call.data == 'Сброс')
def handle_reset_user(call):
    callback.reset_user_chat_id()


@bot.callback_query_handler(lambda call: call.data != 'Сброс')
def handle_set_user(call):
    callback.set_user_chat_id(call.data)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
