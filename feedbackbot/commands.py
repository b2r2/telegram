class HandlerCommands():
    def __init__(self, bot, telebot):
        self.bot = bot
        self.telebot = telebot

    def handle_start(self, message):
        user_markup = self.telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row(u'О канале', u'Отзывы и предложения')
        user_markup.row(u'Условия рекламы', u'Предложить новость')

        msg = u'Доброго времени суток!\nС помощью меня Вы можете связаться'\
            ' с моим создателем и администратором сообщества'\
            ' https://t.me/nuancesprog\nДля этого выберете одно из'\
            'возможных действий!'
        self.bot.send_message(message.from_user.id, msg,
                              reply_markup=user_markup)

    def handle_about(self, message):
        msg = 'Проект создан для программистов любого уровня.\n'\
            'Мы стараемся делиться с вами интересной информацией каждый день!'
        self.bot.send_message(message.from_user.id, msg)

    def handle_feedback(self, message):
        pass

    def handle_advertising(self, message):
        pass

    def handle_suggest(self, message):
        pass
