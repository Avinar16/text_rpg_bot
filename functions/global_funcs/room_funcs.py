import random
from data.items_in_room import Items_in_room
from data.items import Items
from data.mobs_list import Mobs_list
from data.rooms import Rooms
from functions.service_funcs.get_data import *


def add_items(update, context):
    char, db_sess = get_data_character(update, return_sess=True)
    # События
    item_encounter = random.randrange(1, 21)
    item_count = random.randrange(1, 4)

    items_level = [0] * item_count

    # Самый положительный исход
    if item_encounter == 20:
        # add 1 item +2 level and other +0 level
        items_level[0] = 2
    # Положительный исход
    elif item_encounter >= 17:
        # add 1 item +1 and other +0 level
        items_level[0] = 1
    # нейтральный исход
    elif item_encounter > 10:
        # add 1 item +0 and other -1 level
        if char.level != 1:
            items_level = [-1] * item_count
            items_level[0] = 0
    # отрицательный исход
    elif item_encounter >= 6:
        if char.level != 1:
            items_level = [-1] * item_count
    # нет вещей
    else:
        return

    for level in items_level:
        item_level = char.level + level
        if item_level > 10:
            item_level = random.randrange(7, 11)
        suitable_items = db_sess.query(Items).filter(Items.level == item_level).all()
        # находим рандомный итем соответствующий по лвлу
        item = random.choice(suitable_items)

        iir = Items_in_room()
        iir.items = item
        iir.rooms = char.room
        db_sess.add(iir)

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
                if char.level != 1:
                    mobs_level[count] = -1
                else:
                    mobs_level = [2]

    for level in mobs_level:
        mob_baff = False
        mob_level = char.level + level
        if mob_level > 10:
            mob_level = random.randrange(7, 11)
            mob_baff = True
        suitable_mobs = db_sess.query(Mobs_list).filter(Mobs_list.level == mob_level).all()
        # находим рандомного моба соответствующего по лвлу
        mob = random.choice(suitable_mobs)
        Mob = Mobs(
            hp=mob.hp,
            armor=mob.armor,
            attack=mob.attack,
            room_id=room.id
        )
        print(Mob.hp)
        print(Mob.attack)
        if mob_baff:
            Mob.hp = round(Mob.hp * 1.5)
            print(Mob.hp)
            Mob.attack = round(Mob.attack * 1.5)
            print(Mob.attack)
        Mob.mobs = mob
        mob_room = db_sess.query(Rooms).filter(Rooms.id == room.id).first()
        Mob.rooms = mob_room
        db_sess.add(Mob)
        db_sess.commit()
