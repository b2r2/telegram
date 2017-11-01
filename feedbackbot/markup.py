class Markup():
    def __init__(self, telebot):
        self.telebot = telebot

    def get_keyboard(self, **list_commands):
        markup = self.telebot.types.ReplyKeyboardMarkup(True, True)
        markup.row(list_commands['about'], list_commands['feedback'])
        markup.row(list_commands['advertising'], list_commands['suggest'])

        return markup

    def get_inline(self, name_button, cid):
        markup = self.telebot.types.InlineKeyboardMarkup()
        markup.add(self.telebot.types.InlineKeyboardButton(name_button,
                                                           callback_data=str(cid)))

        return markup
