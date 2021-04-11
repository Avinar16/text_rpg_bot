from functions.service_funcs.registration import register_user
from functions.service_funcs.get_data import get_data_user
from functions.debug_func.user_default import user_default

REGISTER, ENTER, EXIT = range(1, 4)


def start(update, context):
    # Регистрация/приветствие юзера/ отправка клавиатуры
    register_user(update)

    # Запуск флага "in_game"
    user, db_sess = get_data_user(update, return_sess=True)
    user.in_game = True
    db_sess.commit()

    # user_default(update)
    update.message.reply_text("""Как назвать вашего персонажа?""")
    update.message.reply_text(f'user {user.tg_id} in game={user.in_game}')

    # Регистрация персонажа
    return REGISTER


def record(update, context):
    # Вывести рекорд
    best_score = get_data_user(update).best_score
    update.message.reply_text(f'Ваш рекорд - {best_score}')


def help(update, context):
    current_user = get_data_user(update)
    if not current_user.in_game:
        update.message.reply_text(
            """
            /record - Показать рекорд
            """
        )
    else:
        update.message.reply_text(
            """/record - Показать рекорд
/inventory - Открыть инвентарь
/stats - Посмотреть характеристики персонажа"""
        )
        user_default(update)
