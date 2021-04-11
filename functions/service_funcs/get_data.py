from data.users import User
from data.character import Character
from data import db_session


def get_data_user(update, return_sess=False):
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    if return_sess:
        return current_user, db_sess
    return current_user


def get_data_character(update):
    db_sess = db_session.create_session()
    current_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    return current_char
