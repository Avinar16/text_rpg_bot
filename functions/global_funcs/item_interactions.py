from data import db_session
from data.inventory import Inventory
from data.items import Items
from functions.service_funcs.get_data import get_data_character


def drop(id):
    db_sess = db_session.create_session()
    inventory_item = db_sess.query(Inventory).filter(Inventory.item_id == id).first()
    db_sess.delete(inventory_item)
    db_sess.commit()


def equip(update, inv_obj):
    db_sess = db_session.create_session()
    current_char = get_data_character(update)
    item = db_sess.query(Items)
