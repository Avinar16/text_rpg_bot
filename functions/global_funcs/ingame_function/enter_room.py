from functions.service_funcs.create_room import *
from functions.service_funcs.enter_room_checks import *
from functions.global_funcs.fight import start_fight


def enter_room(update, context):
    room = create_room(update, context)

    # levelup+record check
    levelup_check(update, context)
    record_check(update, context)

    return start_fight(update, context)