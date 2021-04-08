from data.users import User
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def register_user(db_sess, update):
    reply_keyboard = [['/help', '/StartGame', '/Record'],
                      ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    user_info = update.effective_user
    db_sess = db_sess.create_session()
    if not db_sess.query(User).filter(User.tg_id == update.effective_user.id).first():
        user = User(
            tg_id=update.effective_user.id,
            score=0,
            best_score=0,
            in_game=False)
        db_sess.add(user)
        db_sess.commit()

    update.message.reply_text(f'Welcome {user_info["first_name"]} {user_info["last_name"]}',
                              reply_markup=markup)


def register_char(update, context, db_session):
    pass
