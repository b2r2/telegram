class Markup():
    """ This method sets keyboard markup """
    def __init__(self, types):
        self.types = types

    def return_keyboard(self, **buttons_name):
        markup = self.types.ReplyKeyboardMarkup(True, True, row_width=2)
        markup.add(buttons_name['about'], buttons_name['feedback'])
        markup.add(buttons_name['advertising'], buttons_name['suggest'])

        return markup

    def return_inline_button(self, button_name, cid):
        markup = self.types.InlineKeyboardMarkup()
        markup.add(self.types.InlineKeyboardButton(button_name,
                                                   callback_data=str(cid)))

        return markup
