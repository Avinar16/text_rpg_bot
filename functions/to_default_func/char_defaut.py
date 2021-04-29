from data.character import Character
from data.inventory import Inventory
from data import db_session
from functions.service_funcs.get_data import get_data_character


def char_default(update, context):
    db_sess = db_session.create_session()
    current_char = get_data_character(update)
    current_char.is_alive = False
    db_sess.commit()
