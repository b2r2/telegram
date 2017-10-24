class CommandsHandler():
    def __init__(self, bot, telebot, settings):
        self.bot = bot
        self.telebot = telebot
        self.settings = settings

    def handle_start(self, message):
        user_markup = self.telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(u'О канале', u'Отзывы и предложения')
        user_markup.row(u'Условия рекламы', u'Предложить новость')

        msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
               'с моим создателем и администратором сообщества ' +
               self.settings.long_link + '\nДля этого выберете одно из '
               'возможных действий!')
        self.bot.send_message(message.from_user.id, msg,
                              reply_markup=user_markup)

    def handle_about(self, message):
        msg = ('Проект создан для программистов любого уровня.\n'
               'Здесь Вы всегда можете узнать что-то новое!\n\n'
               'С помощью меня Вы можете связаться с моим создателем и '
               'администратором сообщества ' + self.settings.short_link +
               '\nДля этого выберете одно из возможных действий из '
               'контекстного меню.')
        self.bot.send_message(message.from_user.id, msg)

    def handle_feedback(self, message):
        msg = ('Вы можете оставить свои отзывы о канале и пожелания.\n'
               'Мы стараемся для Вас!')
        self.bot.send_message(message.from_user.id, msg)

    def handle_advertising(self, message):
        msg = ('Условия рекламы на канале ' + self.settings.short_link +
               '\n\nОтдельный пост: 600 рублей, выход поста 14:00\n'
               'Пост в подборке: 300 рублей, выход поста в 20:00\n\n'
               'Пост не удаляется из ленты, топ от 5 часов.\n\n'
               'Постоянным клиентам и при единовременной покупкe нескольких '
               'постов действует система скидок:\n'
               'От 3 постов - 5%\n'
               'От 5 постов - 7%\n'
               'От 10 постов - 10%\n')
        self.bot.send_message(message.from_user.id, msg)

    def handle_suggest(self, message):
        msg = 'Здесь Вы можете поделиться интересными фактами и событиями.'
        self.bot.send_message(message.from_user.id, msg)
