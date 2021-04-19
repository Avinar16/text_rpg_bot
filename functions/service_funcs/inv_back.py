from functions.global_funcs.ingame_func import inventory
from telegram import ReplyKeyboardMarkup
from data.keyboards import exit_room_keyboard

REGISTER, ENTER, EXIT, INVENTORY, ITEM_INTERACTION = range(1, 6)


def inv_back(update, context, state):
    # Возвращение к инвентарю( к выводу списка )
    if state == INVENTORY:
        return inventory(update, context)
    # Возвращение к комнате
    elif state == EXIT:
        reply_keyboard = exit_room_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text('Возвращаемся  к комнате', reply_markup=markup)
        return state
