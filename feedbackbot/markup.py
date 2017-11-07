class Markup():
    """ This method sets keyboard markup """
    def __init__(self, types):
        self.types = types

    def create_keyboard(self, **buttons):
        markup = self.types.ReplyKeyboardMarkup(True, True, row_width=2)
        markup.add(buttons['about'], buttons['feedback'])
        markup.add(buttons['advertising'], buttons['suggest'])

        return markup

    def create_inline_button(self, button, data):
        markup = self.types.InlineKeyboardMarkup()
        callback = self.types.InlineKeyboardButton(button, callback_data=data)
        markup.add(callback)

        return markup
