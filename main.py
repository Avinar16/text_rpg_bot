# Импортируем необходимые классы.
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler
from data import db_session
from functions.global_funcs.standart_func import *
from functions.global_funcs.ingame_func import *
from functions.service_funcs.registration import register_char

import os

load_dotenv('.env')
db_session.global_init("db/rpg.db")

REGISTER, ENTER, FIGHT, EXIT = range(1, 5)


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(os.getenv("TOKEN"), use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTER: [MessageHandler(filters=Filters.text, callback=register_char)],
            ENTER: [CommandHandler('West', move_between_rooms), CommandHandler('North', move_between_rooms),
                    CommandHandler('East', move_between_rooms)
                    ],
            FIGHT: [CommandHandler('Atack'), fight, CommandHandler('Block'), protection],
            EXIT: [CommandHandler('West', move_between_rooms), CommandHandler('North', move_between_rooms),
                   CommandHandler('East', move_between_rooms)]

        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("record", record))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)

    # Запускаем цикл приема и обработки сообщений.

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
