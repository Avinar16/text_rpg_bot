from data.character import Character
from data.inventory import Inventory
from data import db_session


def char_default(update, context):
    db_sess = db_session.create_session()
    current_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    db_sess.delete(current_char)
    db_sess.commit()
