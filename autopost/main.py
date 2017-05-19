# -*- coding: utf-8 -*-


import telebot
import settings


bot = telebot.TeleBot(settings.token)


def log(message, answer):
    from datetime import datetime
    print("\n --------------------------")
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \n Текст - {3}".format(
        message.from_user.first_name, message.from_user.last_name,
        str(message.from_user.id), message.text))
    print(answer)

chat_id = settings.chat_id
# chat_id = message.from_user_id


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/start', '/stop')
    bot.send_message(message.from_user.id, " Добрый день!\n"
                     "Отсюда можно отправлять сообщения в"
                     " канал {0}".format(chat_id),
                     reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.from_user.id, "Заглушка!")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    answer = "Ты не умеешь играть в эту игру :("
    if message.text.lower() == 'а':
        answer = 'Б'
        bot.send_message(chat_id, answer)
        log(message, answer)
    elif message.text.lower() == 'б':
        answer = 'В'
        bot.send_message(chat_id, answer)
        log(message, answer)
    elif message.text == '/stop':
        pass
    else:
        bot.send_message(chat_id, answer)
        log(message, answer)

bot.polling(none_stop=True, interval=0)
