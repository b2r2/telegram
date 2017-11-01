# -*- coding: utf-8 -*-


import telebot
import commands
import settings
import query
import markup


bot = telebot.TeleBot(settings.token)
markup = markup.Markup(telebot)
commands = commands.CommandsHandler(bot, markup, settings)
callback = query.Callback()


@bot.message_handler(commands=['start'])
def command_start(message):
    commands.handle_chat_action(message)
    commands.handle_start(message)


@bot.message_handler(commands=['about'])
def command_about(message):
    commands.handle_chat_action(message)
    commands.handle_about(message)


@bot.message_handler(commands=['feedback'])
def command_feedback(message):
    commands.handle_chat_action(message)
    commands.handle_feedback(message)


@bot.message_handler(commands=['advertising'])
def command_advertising(message):
    commands.handle_chat_action(message)
    commands.handle_advertising(message)


@bot.message_handler(commands=['suggest'])
def command_suggest(message):
    commands.handle_chat_action(message)
    commands.handle_suggest(message)


@bot.callback_query_handler(lambda call: True)
def handle_callback(call):
    callback.set_user_chat_id(call.data)


@bot.callback_query_handler(lambda call: call.data == 'reset')
def handle_callback(call):
    callback.reset_user_chat_id()


@bot.message_handler(func=lambda message: message.text == 'О канале')
def handle_about(message):
    commands.handle_chat_action(message)
    commands.handle_about(message)


@bot.message_handler(func=lambda message: message.text == 'Отзывы и предложения')
def handle_feedback(message):
    commands.handle_chat_action(message)
    commands.handle_feedback(message)


@bot.message_handler(func=lambda message: message.text == 'Условия рекламы')
def handle_advertising(message):
    commands.handle_chat_action(message)
    commands.handle_advertising(message)


@bot.message_handler(func=lambda message: message.text == 'Предложить новость')
def handle_suggest(message):
    commands.handle_chat_action(message)
    commands.handle_suggest(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    user_chat_id = callback.get_user_chat_id()
    if user_chat_id:
        commands.handle_chat_action(message)
        commands.handle_admin_message(message, user_chat_id)
    else:
        commands.handle_chat_action(message)
        commands.handle_message(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
