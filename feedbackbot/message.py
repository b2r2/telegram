class Message():
    def __init__(self, bot):
        self.bot = bot

    def send_start(self, message, keyboard, INFO):
        self.bot.send_message(chat_id=message.chat.id,
                              text=INFO['start'],
                              reply_markup=keyboard)

    def send_command_message(self, message, text):
        self.bot.send_message(chat_id=message.chat.id,
                              text=text)

    def send_inline_button(self, ADMIN_CHAT_ID, text, button):
        self.bot.send_message(chat_id=ADMIN_CHAT_ID,
                              text=text,
                              reply_markup=button)

    def send_user_message(self, chat_id, text):
        self.bot.send_message(chat_id=chat_id, text=text)

    def forward_message(self, message, ADMIN_CHAT_ID):
        self.bot.forward_message(ADMIN_CHAT_ID,
                                 message.chat.id,
                                 message.message_id)
