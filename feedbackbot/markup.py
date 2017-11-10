from telebot import types


class KeyboardMarkupFactory():
    """ This method sets keyboard markup """

    def create_keyboard(self, **buttons):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           one_time_keyboard=True,
                                           row_width=2)
        markup.add(buttons['about'], buttons['feedback'])
        markup.add(buttons['advertising'], buttons['suggest'])

        return markup

    def create_inline_button(self, button, data):
        markup = types.InlineKeyboardMarkup()
        callback = types.InlineKeyboardButton(text=button, callback_data=data)
        markup.add(callback)

        return markup
