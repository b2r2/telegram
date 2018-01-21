# -*- coding: utf-8 -*-


import utils
from config import GROUP_ID


class MessageHandler():
    def __init__(self, bot):
        self.bot = bot

    def send_command(self, message):
        self.bot.send_message(chat_id=message.chat.id,
                              text=utils.get_command_message(message.text),
                              reply_markup=utils.get_markup(message.text))

    def send_message(self, message):
        try:
            user_chat_id = message.reply_to_message.forward_from.id
        except AttributeError:
            self.bot.send_message(chat_id=message.chat.id,
                                  text='Please select reply message.')
        else:
            self.bot.send_message(chat_id=user_chat_id,
                                  text=message.text)

    def forward_message(self, message):
        self.bot.forward_message(chat_id=GROUP_ID,
                                 from_chat_id=message.chat.id,
                                 message_id=message.message_id)
