from data.character import Character
from data import db_session


def char_default(update):
    db_sess = db_session.create_session()
    current_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    db_sess.delete(current_char)
    db_sess.commit()
    print(f'User {update.effective_user.id} char deleted')
