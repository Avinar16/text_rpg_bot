from data import db_session
import random
from data.mobs import Mobs
from data.rooms import Rooms
from data.room_list import Room_list
from functions.service_funcs.get_data import get_data_character
from data.character import Character


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

    id = random.randrange(1, 10)
    Mob = db_sess.query(Mobs).filter(Mobs.id == 1).first()
    new_room.mobs.append(Mob)
    # /////////////////////
    # add_items
    # //////////////////

    db_sess.add(new_room)
    char.room = new_room

    db_sess.commit()

    return new_room

def create_items_in_room():
    pass