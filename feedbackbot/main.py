# -*- coding: utf-8 -*-


import telebot
import commands
import settings


known_users = []
user_step = {}


def get_user_step(uid):
    if uid in user_step:
        return user_step[uid]
    else:
        known_users.append[uid]
        user_step[uid] = 0
        print("New user detected, who hasn't user \'start' yet")
        return 0


def listener(message):
    """
    When new message arrive Bot will call this function.
    """
    for m in message:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + ' [' + str(m.chat.id) +
                  ']: ' + m.text)


bot = telebot.TeleBot(settings.token)
bot.set_update_listener(listener)  # register listener

commands = commands.CommandsHandler(bot, telebot, settings,
                                    known_users, user_step)


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
    else:
        commands.handle_text(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
