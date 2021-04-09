# Импортируем необходимые классы.
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from data import db_session
from library.registration import register_char, register_user
from library.get_data import get_data_user, get_data_character

# debug funcs
from library.debug_func.user_default import user_default

import os

load_dotenv('.env')
db_session.global_init("db/rpg.db")


def Record(update, context):
    best_score = get_data_user(update).best_score
    update.message.reply_text(f'Ваш рекорд - {best_score}')


# Напишем соответствующие функции.
# Их сигнатура и поведение аналогичны обработчикам текстовых сообщений.
def start(update, context):
    # Регистрация/приветствие юзера/ отправка клавиатуры
    register_user(update)

    # Запуск флага "in_game"
    user, db_sess = get_data_user(update, return_sess=True)
    chracter = get_data_character(update)
    user.in_game = True
    db_sess.commit()

    # user_default(update)
    update.message.reply_text("""Как назвать вашего персонажа?""")
    update.message.reply_text(f'user {user.tg_id} in game={user.in_game}')

    return 1


def help(update, context):
    current_user = get_data_user(update)
    if not current_user.in_game:
        update.message.reply_text(
            """
            /Record - Показать рекорд
            """
        )
    else:
        print(f'player {current_user.id} in game')
        user_default(update)


def ingame_check(update, context):
    current_user = get_data_user(update)
    if current_user.in_game:
        return 1
    else:
        return 2


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(os.getenv("TOKEN"), use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters=Filters.text, callback=register_char)],
            2: [],

        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("Record", Record))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)

    # Запускаем цикл приема и обработки сообщений.

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
