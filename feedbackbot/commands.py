class CommandsHandler():
    def __init__(self, bot, telebot, settings):
        self.bot = bot
        self.telebot = telebot
        self.settings = settings

    def handle_start(self, message):
        user_markup = self.telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(u'О канале', u'Отзывы и предложения')
        user_markup.row(u'Условия рекламы', u'Предложить новость')

        cid = message.chat.id

        msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
               'с моим создателем и администратором сообщества ' +
               self.settings.long_link + '\nДля этого выберете одно из '
               'возможных действий!')
        self.bot.send_message(cid, msg, reply_markup=user_markup)

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

    def handle_text(self, message):
        cid = message.chat.id

        smiley = u'\U0001F609'

        msg = "Ваше сообщение отправлено!\nСпасибо! " + smiley

        markup = self.telebot.types.InlineKeyboardMarkup()
        markup.add(self.telebot.types.InlineKeyboardButton('Ответить',
                                                           callback_data=str(cid)))
        self.bot.send_message(cid, msg)

        mod_text = (message.chat.first_name + ' [' + str(cid) + ']\n' +
                    message.text)

        self.bot.send_message(chat_id=self.settings.target_chat,
                              text=mod_text, disable_notification=True,
                              reply_markup=markup)

    def handle_long_text(self, message):
        cid = message.chat.id
        self.send_chat_action(cid, 'typing')

    def handle_answer(self, message, cid):
        self.bot.send_message(cid, message.text)
