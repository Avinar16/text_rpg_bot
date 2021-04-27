from functions.service_funcs.create_room import *
from functions.global_funcs.fight import fight_handler


def enter_room(update, context):
    room = create_room(update, context)

    # levelup+record check


    # Определение первого хода

    char = get_data_character(update)
    if char.room.mobs:
        db_sess = db_session.create_session()

        mob_info = db_sess.query(Mobs_list).filter(Mobs_list.id == char.room.mobs[0].mob_id).first()
        if mob_info.level > char.level:
            turn = False
        else:
            turn = True
        update.message.reply_text(f'Вы пришли в {room.name} \n{room.description}\n')
    else:
        turn = True

    return fight_handler(update, context, turn)
