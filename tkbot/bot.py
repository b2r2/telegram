# -*- coding: utf-8 -*-

import telebot
import settings
import path
import logging
import utils.handler
import utils.db


class Log():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                                      '# (%(asctime)s)',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        filehandler = logging.FileHandler(path.log)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.ERROR)

        copy_filehandler = logging.FileHandler(path.copy_log)
        copy_filehandler.setFormatter(formatter)
        copy_filehandler.setLevel(logging.ERROR)

        self.logger.addHandler(console)
        self.logger.addHandler(filehandler)
        self.logger.addHandler(copy_filehandler)

    def error(self, function_name, msg):
        self.logger.exception('Error:  %s. Sending a file(type %s)',
                              function_name, msg)

    def info(self, function_name):
        self.logger.info('%s: success', function_name)

##########################################################################

log = Log()
bot = telebot.TeleBot(settings.token)

chat_id = settings.chat_id
db = utils.db.Database()

user_will_send_advertising = set()
user_will_send_channel = set()
user_will_send_schedule = set()


handler = utils.handler.Handler(bot, chat_id, db)


#########################################
@bot.message_handler(commands=['start'])
def handle_Start(message):
    handler.handle_Start(message)


@bot.message_handler(commands=['help'])
def handle_Help(message):
    handler.handle_Help(message)


@bot.message_handler(commands=['mydata'])
def handle_Data(message):
    handler.handle_Data(message)


@bot.message_handler(commands=['advertising', 'channel', 'schedule'])
def handle_Advertising(message):
    if message.text == '/advertising':
        user_will_send_advertising.add(message.from_user.id)
        handler.handle_Advertising(message)

    elif message.text == '/channel':
        user_will_send_channel.add(message.from_user.id)
        handler.handle_Channel(message)

    elif message.text == '/schedule':
        user_will_send_schedule.add(message.from_user.id)
        handler.handle_Schedule(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_advertising)
def handle_Advertising_Message(message):
    # no photo!
    user_will_send_advertising.remove(message.from_user.id)
    handler.handle_Advertising_Message(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_channel)
def handle_Channel_Message(message):
    user_will_send_channel.remove(message.from_user.id)
    handler.handle_Channel_Message(message)


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_schedule)
def handle_Schedule_Message(message):
    user_will_send_schedule.remove(message.from_user.id)
    handler.handle_Schedule_Message(message)


#########################################
@bot.message_handler(content_types=['photo'])
def handle_Photo(message):
    handler.handle_Photo(message)


@bot.message_handler(content_types=['sticker'])
def handle_Sticker(message):
    handler.handle_Sticker(message)


@bot.message_handler(content_types=['audio'])
def handle_Audio(message):
    handler.handle_Audio(message)


@bot.message_handler(content_types=['document'])
def handle_Document(message):
    handler.handle_Document(message)


@bot.message_handler(content_types=['video'])
def handle_Video(message):
    handler.handle_Video(message)


@bot.message_handler(content_types=['text'])
def handle_Text(message):
    handler.handle_Text(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
