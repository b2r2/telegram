# -*- coding: utf-8 -*-


import telebot
import commands
import settings


known_user = []

bot = telebot.TeleBot(settings.token)
commands = commands.CommandsHandler(bot, telebot, settings)


@bot.message_handler(commands=['start'])
def command_start(message):
    commands.handle_start(message)


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


@bot.message_handler(commands=['sendLongText'])
def command_long_text(message):
    commands.handle_long_text(message)


@bot.callback_query_handler(lambda call: True)
def callback_inline(call):
    if call.message:
        known_user.append(int(call.data))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    if message.text == 'О канале':
        commands.handle_about(message)
    elif message.text == 'Отзывы и предложения':
        commands.handle_feedback(message)
    elif message.text == 'Условия рекламы':
        commands.handle_advertising(message)
    elif message.text == 'Предложить новость':
        commands.handle_suggest(message)
    elif known_user:
        commands.handle_answer(message, known_user[-1])
        known_user.pop()
    else:
        commands.handle_text(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
