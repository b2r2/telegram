from telebot import types
from text import INFO
from text import COMMANDS
from config import BUTTON_NAMES
from config import ADVERTISING_LINK


def is_data(message):
    return isinstance(message.data, str) and len(message.data) > 0


def is_command(message):
    return any(message.text in x for x in COMMANDS)


def get_value(text):
    key = get_keys(text)
    return INFO[key]


def get_keys(text):
    for keys in INFO.keys():
        for key in keys:
            if key in text:
                return keys


def get_markup(text):
    command = get_keys(text)
    markup = None
    if command == ('/start',):
        markup = create_keyboard(**BUTTON_NAMES)
    elif command == ('/advertising', u'Условия рекламы'):
        markup = create_url_inline_button(button='Перейти',
                                          url=ADVERTISING_LINK)
    return markup


def get_command_message(text):
    command = get_keys(text)
    return get_value(command)


def get_chat(name):
    chat_name = get_chat(name)
    return chat_name


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


# DELETE
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


if __name__ == '__main__':
    print(is_command('/start'))
