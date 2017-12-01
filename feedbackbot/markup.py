from telebot import types


class KeyboardMarkupFactory():
    """ This method sets keyboard markup """

    def create_keyboard(self, **buttons):
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

    def create_callback_inline_button(self, button, data):
        markup = types.InlineKeyboardMarkup()
        callback = types.InlineKeyboardButton(text=button,
                                              callback_data=data)
        markup.add(callback)

        return markup

    def create_url_inline_button(self, button, url):
        markup = types.InlineKeyboardMarkup()
        url = types.InlineKeyboardButton(text=button,
                                         url=url)
        markup.add(url)

        return markup
