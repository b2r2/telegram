class CommandsHandler():
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings
        self.user_cid = 0

    def handle_start(self, message, keyboard):
        cid = message.chat.id

        msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
               'с моим создателем и администратором сообщества ' +
               self.settings.long_link + '\nДля этого выберете одно из '
               'возможных действий!')
        self.bot.send_message(cid, msg, reply_markup=keyboard)

    def handle_about(self, message):
        cid = message.chat.id

        msg = ('Проект создан для программистов любого уровня.\n'
               'Здесь Вы всегда можете узнать что-то новое!\n\n'
               'С помощью меня Вы можете связаться с моим создателем и '
               'администратором сообщества ' + self.settings.short_link +
               '\nДля этого выберете одно из возможных действий из '
               'контекстного меню.')
        self.bot.send_message(cid, msg)

    def handle_feedback(self, message):
        cid = message.chat.id

        msg = ('Вы можете оставить свои отзывы о канале и пожелания.\n'
               'Мы стараемся для Вас!')
        self.bot.send_message(cid, msg)

    def handle_advertising(self, message):
        cid = message.chat.id

        msg = ('Условия рекламы на канале ' + self.settings.short_link +
               '\n\nОтдельный пост: 1000 рублей, выход поста 14:00\n'
               'Пост в подборке: 500 рублей, выход поста в 20:00\n\n'
               'Пост не удаляется из ленты, топ от 5 часов.\n\n'
               'Постоянным клиентам и при единовременной покупкe нескольких '
               'постов действует система скидок:\n'
               'От 3 постов - 5%\n'
               'От 5 постов - 7%\n'
               'От 10 постов - 10%\n')
        self.bot.send_message(cid, msg)

    def handle_suggest(self, message):
        cid = message.chat.id

        msg = 'Здесь Вы можете поделиться интересными фактами и событиями.'
        self.bot.send_message(cid, msg)

    def handle_message(self, message):
        cid = message.chat.id
        smiley = u'\U0001F609'
        msg = "Ваше сообщение отправлено!\nСпасибо! " + smiley
        self.bot.send_message(cid, msg)

    def handle_forward_message(self, message):
        self.bot.forward_message(self.settings.target_chat,
                                 message.chat.id, message.message_id)

    def handle_admin_message(self, message, cid):
        self.bot.send_message(cid, message.text)

    def handle_button(self, message, text, inline_button):
        self.bot.send_message(chat_id=self.settings.target_chat,
                              text=text,
                              reply_markup=inline_button)

    def handle_action_callback(self, text, call_data=''):
        self.bot.send_message(self.settings.target_chat,
                              text + call_data)

    def handle_ignore(self, message):
        cid = message.chat.id
        smiley = u'\U0001F609'
        msg = 'Извините, но я различаю только текст и смайлики ' + smiley
        self.bot.send_message(cid, msg)

    def handle_set_user_cid(self, cid):
        self.user_cid = int(cid)

    def handle_reset_user_cid(self):
        self.user_cid = 0

    def handle_return_user_cid(self):
        return self.user_cid
