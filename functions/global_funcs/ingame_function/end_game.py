from functions.service_funcs.create_room import *
from telegram.ext import ConversationHandler
from functions.to_default_func.char_defaut import char_default
from telegram import ReplyKeyboardMarkup
from data.keyboards import not_in_game_keyboard
from functions.service_funcs.timer import remove_job_if_exists


def end_game(update, context):
    print('ENDED')
    db_sess = db_session.create_session()
    # убираем комнату
    clean_room(update)
    chat_id = update.message.chat_id
    remove_job_if_exists(
        str(chat_id),
        context)
    # убираем in_game юзера
    user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    user.in_game = False
    db_sess.commit()

    db_sess.close()

    # убираем персонажа
    char_default(update, context)

    # Клавиатура вне игры
    keyboard = not_in_game_keyboard
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    update.message.reply_text('Игра завершена. Начать новую игру - /start', reply_markup=markup)
    return ConversationHandler.END
