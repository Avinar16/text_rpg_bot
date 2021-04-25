from functions.global_funcs.room_funcs import *
from functions.debug_func.clean_room import clean_room


def create_room(update, context):
    # удаляем старую комнату
    clean_room(update)

    char, db_sess = get_data_character(update, return_sess=True)

    # Создаем новую комнату, записываем ее в базу
    base_room_id = random.randrange(2, 11)
    base = db_sess.query(Room_list).filter(Room_list.id == base_room_id).first()

    new_room = Rooms(
        base_id=base_room_id,
        name=base.name,
        description=base.description
    )
    char.room = new_room
    db_sess.add(new_room)
    db_sess.commit()

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
