# -*- coding: utf-8 -*-


import telebot
import commands
import settings


bot = telebot.TeleBot(settings.token)
commands = commands.CommandsHandler(bot, telebot, settings)


@bot.message_handler(commands=['start'])
def handle_start(message):
    commands.handle_start(message)


@bot.message_handler(commands=['about'])
def handle_about(message):
    commands.handle_about(message)


@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
    commands.handle_feedback(message)


@bot.message_handler(commands=['advertising'])
def handle_advertising(message):
    commands.handle_advertising(message)


@bot.message_handler(commands=['suggest'])
def handle_suggest(message):
    commands.handle_suggest(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'О канале':
        commands.handle_about(message)
    elif message.text == 'Отзывы и предложения':
        commands.handle_feedback(message)
    elif message.text == 'Условия рекламы':
        commands.handle_advertising(message)
    elif message.text == 'Предложить новость':
        commands.handle_suggest(message)
    else:
        bot.forward_message(chat_id=settings.target_chat,
                            from_chat_id=message.chat.id,
                            message_id=message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
