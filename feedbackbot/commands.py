class CommandsHandler():
    def __init__(self, bot, settings, json):
        self.bot = bot
        self.settings = settings
        self.user_cid = 0
        self.json = json

    def handle_start(self, message, keyboard):
        cid = message.chat.id

        msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
               u'с моим создателем и администратором сообщества ' +
               self.settings.long_link + u'\nДля этого выберете одно из '
               u'возможных действий!')
        self.bot.send_message(cid, msg, reply_markup=keyboard)

    def handle_about(self, message):
        cid = message.chat.id

        msg = (u'Проект создан для программистов любого уровня.\n'
               u'Здесь Вы всегда можете узнать что-то новое!\n\n'
               u'С помощью меня Вы можете связаться с моим создателем и '
               u'администратором сообщества ' + self.settings.short_link +
               u'\nДля этого выберете одно из возможных действий из '
               u'контекстного меню.')
        self.bot.send_message(cid, msg)

    def handle_feedback(self, message):
        cid = message.chat.id

        msg = (u'Вы можете оставить свои отзывы о канале и пожелания.\n'
               u'Мы стараемся для Вас!')
        self.bot.send_message(cid, msg)

    def handle_advertising(self, message):
        cid = message.chat.id

        msg = (u'Условия рекламы на канале ' + self.settings.short_link +
               u'\n\nОтдельный пост: 1000 рублей, выход поста 14:00\n'
               u'Пост в подборке: 500 рублей, выход поста в 20:00\n\n'
               u'Пост не удаляется из ленты, топ от 5 часов.\n\n'
               u'Постоянным клиентам и при единовременной покупкe нескольких '
               u'постов действует система скидок:\n'
               u'От 3 постов - 5%\n'
               u'От 5 постов - 7%\n'
               u'От 10 постов - 10%\n')
        self.bot.send_message(cid, msg)

    def handle_suggest(self, message):
        cid = message.chat.id

        msg = u'Здесь Вы можете поделиться интересными фактами и событиями.'
        self.bot.send_message(cid, msg)

    def handle_message(self, message):
        cid = message.chat.id
        smiley = u'\U0001F609'
        msg = u'Ваше сообщение отправлено!\nСпасибо! ' + smiley
        self.bot.send_message(cid, msg)

    def handle_forward_message(self, message):
        self.bot.forward_message(self.settings.target_chat,
                                 message.chat.id, message.message_id)

    def handle_admin_message(self, message, cid):
        self.bot.send_message(cid, message.text)

    def handle_button(self, text, inline_button):
        self.bot.send_message(chat_id=self.settings.target_chat,
                              text=text,
                              reply_markup=inline_button)

    def handle_ignore(self, message):
        cid = message.chat.id
        smiley = u'\U0001F609'
        msg = u'Извините, но я различаю только текст и смайлики ' + smiley
        self.bot.send_message(cid, msg)

    def handle_set_user_cid(self, cid):
        self.user_cid = cid

    def handle_reset_user_cid(self):
        self.user_cid = 0

    def handle_return_user_cid(self):
        return self.user_cid

    def handle_serialization_message(self, message, button):
        msg_data = {
            'name': message.chat.first_name,
            'cid': message.chat.id,
            'action': button
        }
        return self.json.dumps(msg_data)

    def handle_deserialization_message(self, callback_data):
        return self.json.loads(callback_data)
