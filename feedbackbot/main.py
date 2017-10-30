# -*- coding: utf-8 -*-


import telebot
import commands
import settings


known_user = 0

bot = telebot.TeleBot(settings.token)
commands = commands.CommandsHandler(bot, telebot, settings)


@bot.message_handler(commands=['start'])
def command_start(message):
    commands.handle_start(message)


@bot.callback_query_handler(lambda call: True)
def callback_inline(call):
    global known_user
    known_user = int(call.data)


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
def handle_text(message):
    global known_user
    if known_user:
        commands.handle_answer(message, known_user)
        known_user = 0
    else:
        commands.handle_text(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
