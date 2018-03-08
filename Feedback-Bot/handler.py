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

    def sending(self, message):
        user_chat_id = utils.get_chat_id(message)
        if user_chat_id is None:
            self.send_error(message.chat.id,
                            'Please select reply message')
        elif message.text:
            self.__send_message(user_chat_id, message.text)
        elif message.photo:
            self.__send_photo(user_chat_id, message.photo[0].file_id)
        elif message.sticker:
            self.__send_sticker(user_chat_id, message.sticker.file_id)

    def __send_message(self, user_chat_id, text):
        self.bot.send_message(chat_id=user_chat_id,
                              text=text)

    def __send_photo(self, user_chat_id, photo):
        self.bot.send_photo(chat_id=user_chat_id,
                            photo=photo)

    def __send_sticker(self, user_chat_id, sticker):
        self.bot.send_sticker(chat_id=user_chat_id,
                              data=sticker)

    def send_error(self, chat_id, text):
        self.bot.send_message(chat_id=chat_id,
                              text=text)

    def forward_message(self, message):
        self.bot.forward_message(chat_id=GROUP_ID,
                                 from_chat_id=message.chat.id,
                                 message_id=message.message_id)
