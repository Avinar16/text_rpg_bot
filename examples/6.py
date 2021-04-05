from telegram.ext import Updater, CommandHandler, ConversationHandler
from dotenv import load_dotenv
import os

load_dotenv()


def start(update, context):
    update.message.reply_text("Для входа в музей введите команду /enter.")


def to_enter(update, context):
    update.message.reply_text("Добро пожаловать! Не забудьте сдать вещи в гардероб.")
    update.message.reply_text("Вы находитесь в зале №1. Здесь представлено чучело мамонта.")
    update.message.reply_text("Отсюда можно выйти (/exit) или перейти в зал №2 (/to2).")
    return 1


def to_1(update, context):
    update.message.reply_text("Вы находитесь в зале №1. Здесь представлено чучело мамонта.")
    update.message.reply_text("Отсюда можно выйти (/exit) или перейти в зал №2 (/to2).")
    return 1


def to_2(update, context):
    update.message.reply_text("Вы находитесь в зале №2. Здесь представлено жилище пещерного человека.")
    update.message.reply_text("Отсюда можно перейти в зал №3 (/to3).")
    return 2


def to_3(update, context):
    update.message.reply_text("Вы находитесь в зале №3. Здесь представлены орудия труда каменного века.")
    update.message.reply_text("Отсюда можно перейти в зал №4 (/to4) или в зал №1 (/to1).")
    return 3


def to_4(update, context):
    update.message.reply_text("Вы находитесь в зале №4. Здесь представлена неведомая диковина, найденная археологами.")
    update.message.reply_text("Отсюда можно перейти в зал №1 (/to1).")
    return 4


def to_exit(update, context):
    update.message.reply_text("Всего доброго! Не забудьте забрать вещи из гардероба.")
    return ConversationHandler.END


def main():
    updater = Updater(os.getenv("TOKEN"), use_context=True)
    dp = updater.dispatcher

    museum_handler = ConversationHandler(
        entry_points=[CommandHandler('enter', to_enter), CommandHandler('start', start)],

        states={
            1: [CommandHandler('to2', to_2), CommandHandler('exit', to_exit)],
            2: [CommandHandler('to3', to_3)],
            3: [CommandHandler('to1', to_1), CommandHandler('to4', to_4)],
            4: [CommandHandler('to1', to_1)]
        },
        fallbacks=[]
    )

    dp.add_handler(museum_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
