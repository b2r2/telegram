# -*- coding: utf-8 -*-


import telebot
import settings


bot = telebot.TeleBot(settings.token)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.forward_message(chat_id=settings.target_chat,
                        from_chat_id=message.chat.id,
                        message_id=message.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
