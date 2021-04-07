# Импортируем необходимые классы.
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import db_session
from data.users import User
from library.register_user import register
from library.Game import Game

import os

load_dotenv('.env')
db_session.global_init("db/rpg.db")


def StartGame(update, context):
    db_sess = db_session.create_session()
    Game(update)
    update.message.reply_text('Здесь могла бы быть ваша реклама')


def Record(update, context):
    best_score = get_data(update).best_score
    update.message.reply_text(f'Ваш рекорд - {best_score}')

    return ingame_check(update, context)


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
def start(update, context):
    current_user = get_data(update)
    reply_keyboard = [['/help', '/StartGame', '/Record'],
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Welcome",
        reply_markup=markup
    )
    register(db_session, update)

    return ingame_check(update, context)


def get_data(update):
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    return current_user


def help(update, context):
    current_user = get_data(update)
    if not current_user.in_game:
        update.message.reply_text(
            """
            /StartGame - Начать игру
            /Record - Показать рекорд
            """
        )
    else:
        print(f'player {current_user.id} in game')

    update.message.reply_text("Help ksta")

    return ingame_check(update, context)


def cancel(update, context):
    update.message.reply_text("closed")


def ingame_check(update, context):
    current_user = get_data(update)
    if current_user.in_game:
        return 2
    else:
        return 1


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(os.getenv("TOKEN"), use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [CommandHandler("help", help), CommandHandler("Record", Record),
                CommandHandler("StartGame", StartGame, pass_user_data=True)],
            2: [MessageHandler(Filters.text, help)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Запускаем цикл приема и обработки сообщений.

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
