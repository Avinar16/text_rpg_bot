from functions.service_funcs.get_data import get_data_character
from functions.service_funcs.timer import *


def item_usages(update, context, item):
    char, db_sess = get_data_character(update, return_sess=True)
    context.user_data['task_info'] = {'task': end_timer,
                                      'update': update,
                                      "item": item}
    # Логика лечения от зелий
    if item.name == 'Малое зелье здоровья':
        heal(update, context, char, 6)
    elif item.name == 'Зелье здоровья':
        heal(update, context, char, 10)
    elif item.name == 'Вилка с глазом':
        heal(update, context, char, 3)
    elif item.name == 'Жаренная грязь':
        heal(update, context, char, 5)
    elif item.name == 'Жаренная лапка кролика':
        heal(update, context, char, 10)
    elif item.name == 'Фляга с Эстусом':
        heal(update, context, char, 25)
    elif item.name == 'Собачий корм':
        heal(update, context, char, 55)
    # Логика зелья силы с таймером
    elif item.name == 'Малое зелье силы':
        buff(update, context, char, 4, 40, db_sess)
    elif item.name == 'Зелье силы':
        buff(update, context, char, 8, 40, db_sess)


def end_timer(context):
    # получаем инфу
    job = context.job
    data = job.context.user_data['task_info']
    # Обрабатываем
    char, db_sess = get_data_character(data['update'], return_sess=True)
    item = data['item']
    if 'елье силы' in item.name:
        char.attack -= data['effect']
    db_sess.commit()
    # Выводим текст
    data['update'].message.reply_text(f'Действие эффекта от {item.name} закончилось!')


def heal(update, context, char, effect):
    hp_to_set = (int(char.max_hp) - int(char.hp)) - int(effect)
    if hp_to_set <= 0:
        char.hp = char.max_hp
    else:
        char.hp = char.max_hp - hp_to_set
    update.message.reply_text(f'Вы исцелились. Здоровье {char.hp} / {char.max_hp}')


def buff(update, context, char, effect, duration, db_sess):
    effect = int(effect)
    char.attack += effect
    context.user_data['task_info']['duration'] = duration
    context.user_data['task_info']['effect'] = effect
    db_sess.commit()
    set_timer(update, context)
