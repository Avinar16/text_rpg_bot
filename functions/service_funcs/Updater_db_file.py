from data import db_session
import random
from data.rooms import Rooms
from data.room_list import Room_list
from data.mobs import Mobs
from functions.service_funcs.get_data import *


def create_room(update, context):
    char, db_sess = get_data_character(update, return_sess=True)

    db_sess.delete(char.room)

    # Создаем новую комнату, записываем ее в базу
    base_room_id = random.randrange(2, 11)
    base = db_sess.query(Room_list).filter(Room_list.id == base_room_id).first()

    new_room = Rooms(
        base_id=base_room_id,
        name=base.name,
        description=base.description
    )

    # /////////////////////
    # add_items
    # //////////////////

    db_sess.add(new_room)
    char.room = new_room

    db_sess.commit()

    return new_room


def create_items_in_room():
    pass

def death_char_delete_room(update, context, mob):
    char, db_sess = get_data_character(update, return_sess=True)
    db_sess.delete(char.room)
    mob_murder = db_sess.query(Mobs).filter(Mobs.mob_id == mob.mob_id).first()
    db_sess.delete(mob_murder)
    update.message.reply_text(f'{char.name} погиб!')
    db_sess.commit()

