from functions.service_funcs.get_data import get_data_character


def clean_room(update):
    char, db_sess = get_data_character(update, return_sess=True)
    # удаляем старую комнату и всю инфу о ней
    for mob in char.room.mobs:
        db_sess.delete(mob)
    for item in char.room.items:
        db_sess.delete(item)
    db_sess.delete(char.room)
    db_sess.commit()
