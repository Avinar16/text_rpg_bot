from data import db_session
import random
from data.character import Character


def update_room(update, room_id, user_id):
    db_sess = db_session.create_session()
    new_room_id = random.randrange(1, 11)
    user_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    setattr(user_char, 'room_id', new_room_id)
    db_sess.commit()
