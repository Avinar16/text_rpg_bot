from functions.service_funcs.get_data import *


def print_stats(update, context):
    # Вывод статов
    current_char = get_data_character(update)
    update.message.reply_text(f'''
Персонаж {current_char.name}, {current_char.level}lvl
HP - {current_char.hp} / {current_char.max_hp}
Attack - {current_char.attack}
Armor - {current_char.armor}
Exp - {current_char.exp}''', )
