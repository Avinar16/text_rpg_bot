from functions.global_funcs.ingame_function.in_game_inv import inventory
from ..service_funcs.get_data import get_data_character
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
            return fight_handler(update, context, True)
        else:
            return loot_handler(update, context)
