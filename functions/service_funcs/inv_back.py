from functions.global_funcs.ingame_function.in_game_inv import inventory
from telegram import ReplyKeyboardMarkup
from ..service_funcs.get_data import get_data_character
from data.keyboards import exit_room_keyboard
from ..global_funcs.fight import fight_handler
from data.states import *
from ..global_funcs.loot import loot_handler


def inv_back(update, context, state):
    # Возвращение к инвентарю( к выводу списка )
    if state == INVENTORY:
        return inventory(update, context)
    # Возвращение к комнате
    elif state == EXIT:
        update.message.reply_text('Возвращаемся')
        if get_data_character(update).room.mobs:
            update.message.reply_text('Пока вы ковырялись в сумке, мобы напали!')
            return fight_handler(update, context, False)
        else:

            return loot_handler(update, context)
        return EXIT
