from data import db_session
from functions.service_funcs.get_data import get_data_character

def User_Interaction_with_Character(update, context):
    db_sess = db_session.create_session()
    user_info = update.effective_user
    current_user = get_data_character(update)
