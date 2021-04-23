import random
from data.mobs import Mobs
from data.mobs_list import Mobs_list
from data.rooms import Rooms
from functions.service_funcs.get_data import *
from data import db_session


def add_items(update, context):
    # События
    item_encounter = random.randrange(1, 22)
    item_count = random.randrange(1, 4)

    # худший исход
    if item_encounter <= 6:
        # no items
        pass
    # Самый положительный исход
    elif item_encounter == 21:
        # add 1 item +2 level and other +0 level
        pass
    # положительный исход
    elif item_encounter >= 17:
        # add 1 item +1 and other +0 level
        pass
    # отрицательный исход
    else:
        # add 1 item +0 and other -1 level
        pass


def add_mobs(update, context, room):
    char, db_sess = get_data_character(update, return_sess=True)

    # События
    mobs_encounter = random.randrange(1, 22)
    mob_count = random.randrange(1, 4)

    # левелы мобов
    mobs_level = [1] * mob_count

    # Самый положительный исход
    if mobs_encounter >= 18:
        # врагов нет
        update.message.reply_text(f'Кажется, вам повезло. В комнате никого не оказалось.')
        return
    # Положительный исход
    elif mobs_encounter >= 13:
        # add mobs -1 level
        for level in mobs_level:
            if level != 0:
                level -= 1
    # Отрицательный исход
    elif mobs_encounter <= 6:
        first = True
        # add 1 mob +2 level other +1
        for level in mobs_level:
            if first:
                level += 2
                first = False
            else:
                level += 1

    for level in mobs_level:
        # находим рандомного моба соответствующего по лвлу
        mob = db_sess.query(Mobs_list).filter(Mobs_list.id == random.randrange(1, 2),
                                              Mobs_list.level == level).first()
        Mob = Mobs(
            hp=mob.hp,
            armor=mob.armor,
            attack=mob.attack,
            room_id=room.id
        )
        Mob.mobs = mob
        mob_room = db_sess.query(Rooms).filter(Rooms.id == room.id).first()
        Mob.rooms = mob_room
        db_sess.add(Mob)
        db_sess.commit()
