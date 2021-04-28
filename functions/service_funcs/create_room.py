from functions.global_funcs.room_funcs import *
from functions.to_default_func.clean_room import clean_room
from functions.service_funcs.enter_room_checks import *
from data.room_list import Room_list
import random


def create_room(update, context):
    # удаляем старую комнату
    clean_room(update)

    char, db_sess = get_data_character(update, return_sess=True)
    room = random.choice(db_sess.query(Room_list).all())
    # Создаем новую комнату, записываем ее в базу

    new_room = Rooms(
        base_id=room.id,
        name=room.name,
        description=room.description
    )

    levelup_check(update, context)
    record_check(update, context)

    char.room = new_room
    db_sess.add(new_room)
    db_sess.commit()
    if not new_room.base_id == 14:
        add_mobs(update, context, new_room)
    add_items(update, context)

    return new_room


def death_char_delete_room(update, context, mob):
    char, db_sess = get_data_character(update, return_sess=True)
    db_sess.delete(char.room)
    mob_murder = db_sess.query(Mobs).filter(Mobs.mob_id == mob.mob_id).first()
    db_sess.delete(mob_murder)
    update.message.reply_text(f'{char.name} погиб!')
    db_sess.commit()
