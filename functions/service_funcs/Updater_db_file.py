from data import db_session
from data.character import Character


def update_room(update, room_id, user_id):
    db_sess = db_session.create_session()
    user_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    setattr(user_char, 'room_id', user_char.room_id + 1)
    db_sess.commit()
