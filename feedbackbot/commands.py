class CommandsHandler():
    def __init__(self, bot, markup, settings):
        self.bot = bot
        self.markup = markup
        self.settings = settings

    def handle_start(self, message):

        cid = message.chat.id

        list_commands = {
            'about': u'О канале',
            'feedback': u'Отзывы и предложения',
            'advertising': u'Условия рекламы',
            'suggest': u'Предложить новость'
        }
        keyboard_markup = self.markup.get_keyboard(**list_commands)

        msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
               'с моим создателем и администратором сообщества ' +
               self.settings.long_link + '\nДля этого выберете одно из '
               'возможных действий!')
        self.bot.send_message(cid, msg, reply_markup=keyboard_markup)

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

        button = 'Ответить ' + message.chat.first_name
        inline_markup = self.markup.get_inline(button, cid)

        self.bot.send_message(chat_id=self.settings.target_chat,
                              text='Новое сообщение!', disable_notification=True,
                              reply_markup=inline_markup)

        self.bot.forward_message(self.settings.target_chat,
                                 cid, message.message_id)

    def handle_admin_message(self, message, cid):
        button = 'reset'
        inline_markup = self.markup.get_inline(button, button)
        self.bot.send_message(cid, message.text, reply_markup=inline_markup)

    def handle_chat_action(self, message):
        cid = message.chat.id
        self.bot.send_chat_action(cid, 'typing')
