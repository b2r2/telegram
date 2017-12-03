# -*- coding: utf-8 -*-


from telebot import types


class KeyboardMarkupFactory():
    """ Create objects custom keyboard and inline buttons """

    @staticmethod
    def create_keyboard(**buttons):
        """ Create objects custom keyboard """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=False,
                                           row_width=2)
        about = types.KeyboardButton(buttons['about'])
        feedback = types.KeyboardButton(buttons['feedback'])
        advertising = types.KeyboardButton(buttons['advertising'])
        suggest = types.KeyboardButton(buttons['suggest'])

        markup.add(about, feedback)
        markup.add(advertising, suggest)

        return markup

    @staticmethod
    def create_callback_inline_button(button, data):
        """ Create objects custom inline callback button """
        markup = types.InlineKeyboardMarkup()
        callback = types.InlineKeyboardButton(text=button,
                                              callback_data=data)
        markup.add(callback)

        return markup

    @staticmethod
    def create_url_inline_button(button, url):
        """ Create objects custom inline url button """
        markup = types.InlineKeyboardMarkup()
        url = types.InlineKeyboardButton(text=button,
                                         url=url)
        markup.add(url)

        return markup
