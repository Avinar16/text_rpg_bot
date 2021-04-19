from data import db_session
from functions.service_funcs.get_data import get_data_rooms
from functions.service_funcs.Updater_db_file import update_room
from functions.service_funcs.get_data import get_data_character


def inventory(update, context):
    pass


def print_stats(update, context):
    pass


def move_between_rooms(update, context):
    user = get_data_character(update)
    update_room(update, user.room_id, user.user_id)
    user_room = get_data_rooms(user.room_id)
    update.message.reply_text(f'Вы пришли в:{user_room.name, user_room.description}')



def fight(update, context):
    pass


def protection(update, context):
    pass
