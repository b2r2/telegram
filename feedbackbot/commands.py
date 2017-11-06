import json


class CommandsHandler():
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.user_cid = 0

    def handle_start(self, message, keyboard):
        cid = message.chat.id

        msg = (u'Доброго времени суток!\nС помощью меня Вы можете связаться '
               u'с моим создателем и администратором сообщества ' +
               self.config.LINK + u'\nДля этого выберете одно из '
               u'возможных действий!')
        self.bot.send_message(cid, msg, reply_markup=keyboard)

    def handle_about(self, message):
        cid = message.chat.id

        msg = (u'Проект создан для программистов любого уровня.\n'
               u'Здесь Вы всегда можете узнать что-то новое!\n\n'
               u'С помощью меня Вы можете связаться с моим создателем и '
               u'администратором сообщества ' + self.config.SHORT_LINK +
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

        msg = (u'Условия рекламы на канале ' + self.config.SHORT_LINK +
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
        if cid == self.config.ADMIN_CHAT_ID:
            pass
        else:
            self.bot.send_message(cid, msg)

    def handle_forward_message(self, message):
        if message.chat.id != self.config.ADMIN_CHAT_ID:
            self.bot.forward_message(self.config.ADMIN_CHAT_ID,
                                     message.chat.id, message.message_id)

    def handle_admin_message(self, cid, message):
        self.bot.send_message(cid, message.text)

    def handle_button(self, text, inline_button):
        self.bot.send_message(chat_id=self.config.ADMIN_CHAT_ID,
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
        return json.dumps(msg_data)

    def handle_deserialization_message(self, callback_data):
        return json.loads(callback_data)
