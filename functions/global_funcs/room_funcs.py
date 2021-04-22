import random


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


def add_mobs(update, context):
    mobs_encounter = random.randrange(1, 22)
    mob_count = random.randrange(1, 4)

    if mobs_encounter >= 18:
        update.message.reply_text(f'Кажется, вам повезло. В комнате никого не оказалось.')
    elif mobs_encounter >= 13:
        # add mobs -1 level
        pass
    elif mobs_encounter >= 7:
        # add mobs +0 level
        pass
    elif mobs_encounter <= 6:
        pass
        # add 1 mob +2 level other +1
