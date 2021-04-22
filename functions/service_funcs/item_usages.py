from data import db_session
from functions.service_funcs.get_data import get_data_character
from functions.service_funcs.timer import *


def item_usages(update, context, item):
    char, db_sess = get_data_character(update, return_sess=True)
    if item.name == 'Малое зелье здоровья':
        hp_to_set = (char.max_hp - char.hp) - 2
        if hp_to_set <= 0:
            char.hp = char.max_hp
        else:
            char.hp = char.max_hp - hp_to_set
        update.message.reply_text(f'Вы исцелились. Здоровье {char.hp} / {char.max_hp}')
    elif item.name == 'Малое зелье силы':
        print('go')
        print(char.attack)
        char.attack += 2
        print(char.attack)
        context.user_data['task'] = (small_strenght_potion, 30)
        set_timer(update=update, context=context)
    db_sess.commit()


def small_strenght_potion(update, context):
    char, db_sess = get_data_character(update, return_sess=True)
    char.attack -= 2
    db_sess.commit()
    update.message.reply_text('Done')
