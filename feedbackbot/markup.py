class Markup():
    """ This method sets keyboard markup """
    def __init__(self, types):
        self.types = types

    def return_keyboard(self, **buttons):
        markup = self.types.ReplyKeyboardMarkup(True, True, row_width=2)
        markup.add(buttons['about'], buttons['feedback'])
        markup.add(buttons['advertising'], buttons['suggest'])

        return markup

    def return_inline_button(self, button, data):
        markup = self.types.InlineKeyboardMarkup()
        markup.add(self.types.InlineKeyboardButton(button,
                                                   callback_data=str(data)))

        return markup
