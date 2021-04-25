from functions.service_funcs.create_room import *
from telegram.ext import ConversationHandler
from functions.debug_func.char_defaut import char_default


def end_game(update, context):
    db_sess = db_session.create_session()
    # убираем комнату
    clean_room(update)
    # убираем персонажа
    char_default(update)
    # убираем in_game юзера
    user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    user.in_game = False
    db_sess.commit()
    update.message.reply_text('Игра завершена. Начать новую игру - /start')
    return ConversationHandler.END
