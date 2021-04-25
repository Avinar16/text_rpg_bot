from functions.service_funcs.registration import register_user
from functions.service_funcs.get_data import get_data_user
from data.states import *


def start(update, context):
    # Регистрация/приветствие юзера/ отправка клавиатуры
    register_user(update)

    # Запуск флага "in_game"
    user, db_sess = get_data_user(update, return_sess=True)
    user.in_game = True
    db_sess.commit()

    # user_default(update)
    update.message.reply_text("""Как назвать вашего персонажа?""")

    # Регистрация персонажа
    return REGISTER


def record(update, context):
    # Вывести рекорд
    user = get_data_user(update)
    result = f'Ваш рекорд - {user.best_score}\n'
    if user.in_game:
        result += f'Текущий счет комнат - {user.score}'
    update.message.reply_text(result)


def help(update, context):
    current_user = get_data_user(update)
    if not current_user.in_game:
        update.message.reply_text(
            """/start - начать игру
/record - Показать рекорд"""
        )
    else:
        update.message.reply_text(
            """/record - Показать рекорд
/inventory - Открыть инвентарь
/stats - Посмотреть характеристики персонажа
/ end_game - Завершить игру"""
        )
