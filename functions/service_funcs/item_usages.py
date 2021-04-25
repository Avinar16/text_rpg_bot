from functions.service_funcs.get_data import get_data_character
from functions.service_funcs.timer import *


def item_usages(update, context, item):
    char, db_sess = get_data_character(update, return_sess=True)
    context.user_data['task_info'] = {'task': end_timer,
                                      'update': update,
                                      "item": item}
    if item.name == 'Малое зелье здоровья':
        # Логика лечения от зелья
        hp_to_set = (char.max_hp - char.hp) - 2
        if hp_to_set <= 0:
            char.hp = char.max_hp
        else:
            char.hp = char.max_hp - hp_to_set
        update.message.reply_text(f'Вы исцелились. Здоровье {char.hp} / {char.max_hp}')
    # Логика зелья силы с таймером
    elif item.name == 'Малое зелье силы':
        char.attack += 2
        # Вся инфа необходимая для обработки
        context.user_data['task_info']['duration'] = 40
        db_sess.commit()
        set_timer(update, context)


def end_timer(context):
    # получаем инфу
    job = context.job
    data = job.context.user_data['task_info']
    # Обрабатываем
    char, db_sess = get_data_character(data['update'], return_sess=True)
    item = data['item']
    if item.name == 'Малое зелье силы':
        char.attack -= 2
    db_sess.commit()
    # Выводим текст
    data['update'].message.reply_text(f'Действие эффекта от {item.name} закончилось!')
