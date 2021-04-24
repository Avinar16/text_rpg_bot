import random
from data.mobs import Mobs
from data.items import Items
from data.mobs_list import Mobs_list
from data.rooms import Rooms
from functions.service_funcs.get_data import *
from data import db_session


def add_items(update, context):
    char, db_sess = get_data_character(update, return_sess=True)
    # События
    item_encounter = random.randrange(1, 22)
    item_count = random.randrange(1, 4)

    items_level = [0] * item_count

    # худший исход
    if item_encounter <= 6:
        # no items
        return
    # Самый положительный исход
    elif item_encounter == 21:
        # add 1 item +2 level and other +0 level
        items_level[0] = 2
    # положительный исход
    elif item_encounter >= 17:
        # add 1 item +1 and other +0 level
        items_level[0] = 1
    # отрицательный исход
    else:
        # add 1 item +0 and other -1 level
        if char.level != 1:
            items_level = [-1] * item_count
            items_level[0] = 0
    print(item_encounter)
    for level in items_level:
        suitable_items = db_sess.query(Items).filter(Items.level == char.level + level).all()
        item = random.choice(suitable_items)
        print(item.name)
        char.room.items.append(item)
        db_sess.commit()


def add_mobs(update, context, room):
    char, db_sess = get_data_character(update, return_sess=True)

    # События
    mobs_encounter = random.randrange(1, 22)
    mob_count = random.randrange(1, 4)

    # левелы мобов
    mobs_level = [0] * mob_count

    # Самый положительный исход
    if mobs_encounter >= 18:
        # врагов нет
        update.message.reply_text(f'Кажется, вам повезло. В комнате никого не оказалось.')
        return
    # Положительный исход
    elif mobs_encounter >= 13:
        # add mobs -1 level
        if char.level != 1:
            mobs_level = [-1] * mob_count
    # Отрицательный исход
    elif mobs_encounter <= 6:
        for count in range(len(mobs_level)):
            if count == 0:
                mobs_level[0] = 2
            else:
                mobs_level[count] = 1

    for level in mobs_level:
        suitable_mobs = db_sess.query(Mobs_list).filter(Mobs_list.level == char.level + level).all()
        # находим рандомного моба соответствующего по лвлу
        mob = random.choice(suitable_mobs)
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
