from data.users import User
from data import db_session


def get_data(update, return_sess=False):
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    if return_sess:
        return current_user, db_sess
    return current_user
