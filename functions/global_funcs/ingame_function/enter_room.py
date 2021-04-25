from functions.service_funcs.create_room import *
from data.states import *


def enter_room(update, context):
    room = create_room(update, context)
    update.message.reply_text(f'Вы пришли в {room.name} \n{room.description}')
    return EXIT
