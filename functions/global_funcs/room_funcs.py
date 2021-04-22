import random
from data.mobs import  Mobs
from data.mobs_list import Mobs_list
from functions.service_funcs.get_data import get_data_character
from data import db_session



def add_items(update, context):
    item_encounter = random.randrange(1, 22)
    item_count = random.randrange(1, 4)
    if item_encounter <= 6:
        # no items
        pass
    elif item_encounter == 21:
        # add 1 item +2 level and other +0 level
        pass
    elif item_encounter >= 17:
        # add 1 item +1 and other +0 level
        pass
    else:
        # add 1 item +0 and other -1 level
        pass


def add_mobs(update, context, room_id):
    db_sess = db_session.create_session()
    mobs_encounter = random.randrange(1, 22)
    mob_count = random.randrange(1, 4)

    if mobs_encounter >= 18:
        update.message.reply_text(f'Кажется, вам повезло. В комнате никого не оказалось.')
    elif mobs_encounter >= 13:
        # add mobs -1 level
        mob = db_sess.query(Mobs_list).filter(Mobs_list.id == 1).first()
        Mob = Mobs(
            hp=mob.hp,
            armor=mob.armor,
            attack=mob.attack,
            room_id=room_id,
            mob_id=mob.id
        )
        db_sess.add(Mob)
        db_sess.commit()


    elif mobs_encounter >= 7:
        # add mobs +0 level
        pass
    elif mobs_encounter <= 6:
        pass
        # add 1 mob +2 level other +1
