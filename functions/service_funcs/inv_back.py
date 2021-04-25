from functions.global_funcs.ingame_function.in_game_inv import inventory
from telegram import ReplyKeyboardMarkup
from data.keyboards import exit_room_keyboard
from data.states import *


def inv_back(update, context, state):
    # Возвращение к инвентарю( к выводу списка )
    if state == INVENTORY:
        return inventory(update, context)
    # Возвращение к комнате
    elif state == EXIT:
        reply_keyboard = exit_room_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text('Возвращаемся  к комнате', reply_markup=markup)
        return EXIT
