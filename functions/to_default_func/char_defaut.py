from data.character import Character
from data.inventory import Inventory
from data import db_session
from functions.service_funcs.timer import remove_job_if_exists


def char_default(update, context):
    chat_id = update.message.chat_id
    remove_job_if_exists(
        str(chat_id),
        context)
    db_sess = db_session.create_session()
    current_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    inventory = db_sess.query(Inventory).filter(Inventory.char_id == current_char.id).all()
    db_sess.delete(current_char)
    for item in inventory:
        db_sess.delete(item)
    db_sess.commit()
