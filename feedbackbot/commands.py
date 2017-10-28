import time


class CommandsHandler():
    def __init__(self, bot, telebot, settings,
                 known_users, user_step):
        self.bot = bot
        self.telebot = telebot
        self.settings = settings
        self.known_users = known_users
        self.user_step = user_step

    def handle_start(self, message):
        user_markup = self.telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(u'О канале', u'Отзывы и предложения')
        user_markup.row(u'Условия рекламы', u'Предложить новость')

        cid = message.chat.id
        if cid not in self.known_users:
            self.known_users.append(cid)
            self.user_step[cid] = 0

            msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
                   'с моим создателем и администратором сообщества ' +
                   self.settings.long_link + '\nДля этого выберете одно из '
                   'возможных действий!')
            self.bot.send_message(cid, msg,
                                  reply_markup=user_markup)
        else:
            self.bot.send_message(cid, "Рады, что Вы снова с нами!")

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
        mid = message.message_id

        smiley = u'\U0001F609'
        msg = "Ваше сообщение отправлено!\nСпасибо! " + smiley
        self.bot.send_message(cid, msg)

        self.bot.forward_message(chat_id=self.settings.target_chat,
                                 from_chat_id=cid,
                                 message_id=mid)

    def handle_long_text(message):
        cid = message.chat.id
        self.send_chat_action(cid, 'typing')
        time.sleep(3)
        bot.send_message(cid, '.')
