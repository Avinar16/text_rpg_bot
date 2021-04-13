from data import db_session
from functions.service_funcs.get_data import get_data_user, get_data_character


def inventory(update, context):
    db_sess = db_session.create_session()


def print_stats(update, context):
    db_sess = db_session.create_session()
    current_char = get_data_character()
    update.message.reply_text(f'''HP - {current_char.hp}
Maximum hp - {current_char.max_hp}
Level - {current_char.level}
Exp - {current_char.exp}''', )
