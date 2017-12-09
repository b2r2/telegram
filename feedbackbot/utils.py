from telebot import types


def is_check_data(message):
    return isinstance(message.data, str) and len(message.data) > 0


def create_keyboard(**buttons):
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


def create_callback_inline_button(button, data):
    markup = types.InlineKeyboardMarkup()
    callback = types.InlineKeyboardButton(text=button,
                                          callback_data=data)
    markup.add(callback)

    return markup


def create_url_inline_button(button, url):
    markup = types.InlineKeyboardMarkup()
    callback = types.InlineKeyboardButton(text=button,
                                          url=url)
    markup.add(callback)

    return markup
