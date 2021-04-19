# Импортируем необходимые классы.
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, CommandHandler
from functions.global_funcs.standart_func import *
from functions.global_funcs.ingame_func import *
from functions.global_funcs.inventory import *
from functions.service_funcs.registration import register_char

import os

load_dotenv('.env')
db_session.global_init("db/rpg.db")

REGISTER, ENTER, EXIT, INVENTORY, ITEM_INTERACTION = range(1, 6)


def check_move(update, context):
    pass


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(os.getenv("TOKEN"), use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher
    # Основной хендлер
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            # start state
            REGISTER: [MessageHandler(filters=Filters.text, callback=register_char)],

            # room states
            ENTER: [CommandHandler('West', check_move), CommandHandler('North', check_move),
                    CommandHandler('East', check_move),
                    CommandHandler("stats", print_stats)],
            EXIT: [CommandHandler('West', check_move), CommandHandler('North', check_move),
                   CommandHandler('East', check_move),
                   CommandHandler("inventory", inventory),
                   CommandHandler("stats", print_stats)],
            # Inventory states
            INVENTORY: [MessageHandler(filters=(Filters.text | Filters.command), callback=item_choose)],
            ITEM_INTERACTION: [MessageHandler(filters=(Filters.text | Filters.command), callback=item_interaction)]
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
