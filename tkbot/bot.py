# -*- coding: utf-8 -*-

import telebot
import settings
import path
import utils.db


#########################################################################
# LOG CONFIG ############################################################
#########################################################################

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                              '# (%(asctime)s)',
                              datefmt='%Y-%m-%d %H:%M:%S')

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

filehandler = logging.FileHandler(path.logs)
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)

copy_filehandler = logging.FileHandler(path.copy_logs)
copy_filehandler.setFormatter(formatter)
copy_filehandler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(filehandler)
logger.addHandler(copy_filehandler)

#########################################################################
#  FUNCTIONS ############################################################
#########################################################################


def log_Error(function_name, msg):
    logger.exception('Error:  %s. Sending a file(type %s)',
                     function_name, msg)


def log_Info(function_name):
    logger.info('%s: success', function_name)

##########################################################################

bot = telebot.TeleBot(settings.token)

chat_id = settings.chat_id

user_will_send_advertising = set()
user_will_send_channel = set()
user_will_send_schedule = set()

db = utils.db.Database()

print(db.show_Database())


#########################################
# COMMANDS ##############################
#########################################

@bot.message_handler(commands=['start'])
def handle_Start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/help')
    user_markup.row('/channel', '/schedule')
    user_markup.row('/advertising', '/mydata')

    msg = """Hello!
    \nYou can send message in channel {0}""".format(chat_id)
    bot.send_message(message.from_user.id, msg,
                     reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_Help(message):
    msg = """My options are very limited..."""
    bot.send_message(message.from_user.id, msg)


@bot.message_handler(commands=['mydata'])
def handle_Data(message):
    msg = "Your data is in the format (user ID, channel name,"\
            "advertising message, schedule)"
    bot.send_message(message.from_user.id, msg)
    data = db.return_All_Database_User(message.from_user.id)

    for user_data in data[0][1:-1]:
        bot.send_message(message.from_user.id, user_data)


@bot.message_handler(commands=['advertising', 'channel', 'schedule'])
def handle_Advertising(message):
    if message.text == '/advertising':
        user_will_send_advertising.add(message.from_user.id)
        msg = "Give me your advertising message:"
        bot.send_message(message.from_user.id, msg)

    elif message.text == '/channel':
        user_will_send_channel.add(message.from_user.id)
        msg = "Please enter the name of the channel (e.g. @yourchannel)"
        bot.send_message(message.from_user.id, msg)

    elif message.text == '/schedule':
        user_will_send_schedule.add(message.from_user.id)
        msg = "Here you can set up a schedule to release your" + \
              " advertising message in the system.\n" + \
              "Please enter only the hours without minutes" + \
              " (e.g. 01:00, 23:15, etc.):"
        bot.send_message(message.from_user.id, msg)


#########################################
# DATABASE METHODS ######################
#########################################
@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_advertising)
def handle_Advertising_Message(message):
    # no photo!
    user_will_send_advertising.remove(message.from_user.id)
    bot.send_message(message.from_user.id, "It is your advertising message:")

    db.handler_Adv_Message_User(message.from_user.id,
                                message.text,
                                message.date)

    bot.send_message(message.from_user.id,
                     db.return_Adv_Message_User(message.from_user.id))

    bot.send_message(message.from_user.id, "If you see the erorr,"
                     " try again!")
    print(db.show_Database())


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_channel)
def handle_Channel(message):
    user_will_send_channel.remove(message.from_user.id)
    bot.send_message(message.from_user.id, "It is your channel:")

    db.handler_Channel_User(message.from_user.id,
                            message.text,
                            message.date)

    bot.send_message(message.from_user.id,
                     db.return_Channel_User(message.from_user.id))
    bot.send_message(message.from_user.id, "If you see the error,"
                     " try again!")
    print(db.show_Database())


@bot.message_handler(func=lambda message: message.from_user.id in
                     user_will_send_schedule)
def handle_Schedule(message):
    user_will_send_schedule.remove(message.from_user.id)
    bot.send_message(message.from_user.id, "It's your schedule:")

    db.handle_Schedule_User(message.from_user.id,
                            message.text,
                            message.date)

    bot.send_message(message.from_user.id,
                     db.return_Schedule_User(message.from_user.id))

    bot.send_message(message.from_user.id, "If you see the error,"
                     " try again!")
    print(db.show_Database())


#########################################

@bot.message_handler(content_types=['photo'])
def handle_Photo(message):
    try:
        msg_photo = message.photo[0].file_id
        bot.send_photo(chat_id, msg_photo)
    except Exception as err:
        log_Error(err, handle_Photo.__name__)
    else:
        log_Info(handle_Photo.__name__)


@bot.message_handler(content_types=['sticker'])
def handle_Sticker(message):
    try:
        msg_sticker = message.sticker.file_id
        bot.send_sticker(chat_id, msg_sticker)
    except Exception as err:
        log_Error(err, handle_Sticker.__name__)
    else:
        log_Info(handle_Sticker.__name__)


@bot.message_handler(content_types=['audio'])
def handle_Audio(message):
    try:
        msg_audio = message.audio.file_id
        bot.send_audio(chat_id, msg_audio)
    except Exception as err:
        log_Error(err, handle_Audio.__name__)
    else:
        log_Info(handle_Audio.__name__)


@bot.message_handler(content_types=['document'])
def handle_Document(message):
    try:
        msg_document = message.document.file_id
        bot.send_document(chat_id, msg_document)
    except Exception as err:
        log_Error(err, handle_Document.__name__)
    else:
        log_Info(handle_Document.__name__)


@bot.message_handler(content_types=['video'])
def handle_Video(message):
    try:
        msg_video = message.video.file_id
        bot.send_video(chat_id, msg_video)
    except Exception as err:
        log_Error(err, handle_Video.__name__)
    else:
        log_Info(handle_Video.__name__)


@bot.message_handler(content_types=['text'])
def handle_Text(message):
    try:
        bot.send_message(chat_id, message.text)
    except Exception as err:
        log_Error(err, handle_Text)
    else:
        log_Info(handle_Text.__name__)


# @bot.message_handler(regexp=".*")
# def handleMessage(message):
#     print(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
