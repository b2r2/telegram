from telebot import types
from text import ENGLISH_COMMANDS
from text import RUSSIAN_COMMANDS
from text import DESCRIPTION
from config import ADVERTISING_LINK


TEXT_MESSAGES = dict(zip(zip(ENGLISH_COMMANDS, RUSSIAN_COMMANDS), DESCRIPTION))


def is_data(message):
    return isinstance(message.data, str) and len(message.data) > 0


def is_command(message):
    return any(message.text in x for x in TEXT_MESSAGES.keys())


def get_value(text):
    key = get_keys(text)
    return TEXT_MESSAGES[key]


def get_keys(text):
    for keys in TEXT_MESSAGES.keys():
        for key in keys:
            if key == text:
                return keys


def get_markup(text):
    command = get_keys(text)
    markup = None
    if command == ('/start', None):
        markup = create_keyboard(RUSSIAN_COMMANDS[1:])
    elif command == ('/advertising', u'Условия рекламы'):
        markup = create_url_inline_button(button='Перейти',
                                          url=ADVERTISING_LINK)
    return markup


def get_command_message(text):
    command = get_keys(text)
    return get_value(command[0])


def create_keyboard(commands):
    buttons = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=False,
                                       row_width=2)
    for command in commands:
        buttons.append(types.KeyboardButton(command))

    markup.add(*[btn for btn in buttons[:2]])
    markup.add(*[btn for btn in buttons[2:]])

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
