# Импортируем необходимые классы.
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from functions.global_funcs.standart_func import *
from functions.global_funcs.ingame_function.end_game import end_game
from functions.global_funcs.ingame_function.enter_room import enter_room
from functions.global_funcs.ingame_function.in_game_inv import inventory
from functions.global_funcs.ingame_function.print_stats import print_stats
from functions.global_funcs.inventory import *
from functions.service_funcs.registration import register_char
from functions.global_funcs.fight import enemy_choose, enemy_interaction
from data.states import *
from functions.global_funcs.loot import loot_choose, loot_interaction
import os

load_dotenv('.env')
db_session.global_init("db/rpg.db")


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
            EXIT: [CommandHandler('West', enter_room), CommandHandler('North', enter_room),
                   CommandHandler('East', enter_room), CommandHandler("inventory", inventory)],
            # Fight states
            ENEMY_CHOOSE: [MessageHandler(filters=(Filters.text | Filters.command), callback=enemy_choose)],
            ENEMY_INTERACTION: [MessageHandler(filters=(Filters.text | Filters.command), callback=enemy_interaction)],
            # Loot states
            LOOT_CHOOSE: [MessageHandler(filters=(Filters.text | Filters.command), callback=loot_choose)],
            LOOT_INTERACTION: [MessageHandler(filters=(Filters.text | Filters.command), callback=loot_interaction)],
            # Inventory states
            INVENTORY: [MessageHandler(filters=(Filters.text | Filters.command), callback=item_choose)],
            ITEM_INTERACTION: [MessageHandler(filters=(Filters.text | Filters.command), callback=item_interaction)],
        },
        fallbacks=[CommandHandler('end_game', callback=end_game)],
    )
    dp.add_handler(CommandHandler("stats", print_stats))
    dp.add_handler(CommandHandler("record", record))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(conv_handler)

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
