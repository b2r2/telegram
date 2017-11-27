class SenderMessage():
    def __init__(self, bot):
        self.bot = bot

    def publish_start(self, chat_id, keyboard, text):
        self.bot.send_message(chat_id=chat_id,
                              text=text,
                              reply_markup=keyboard)

    def publish_command_message(self, chat_id, text):
        self.bot.send_message(chat_id=chat_id,
                              text=text)

    def publish_callback_inline_button(self, ADMIN_CHAT_ID, text, button):
        self.bot.send_message(chat_id=ADMIN_CHAT_ID,
                              text=text,
                              reply_markup=button)

    def publish_url_inline_button(self, chat_id, text, button):
        self.bot.send_message(chat_id=chat_id,
                              text=text,
                              reply_markup=button)

    def publish_message(self, chat_id, text):
        self.bot.send_message(chat_id=chat_id,
                              text=text)

    def forward_message(self, ADMIN_CHAT_ID, message):
        self.bot.forward_message(chat_id=ADMIN_CHAT_ID,
                                 from_chat_id=message.chat.id,
                                 message_id=message.message_id)

    def publish_answer_callback_query(self, data, text):
        self.bot.answer_callback_query(callback_query_id=data.id,
                                       text=text,
                                       show_alert=False)
