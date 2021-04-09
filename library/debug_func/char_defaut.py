from data.character import Character
from data import db_session

def char_default(update):
    db_sess = db_session.create_session()
    current_user = db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first()
    current_user.id = 0
    current_user.user_id = 0
    current_user.name = ''
    current_user.room_id = 0
    current_user.hp = 0
    current_user.max_hp = 0
    db_sess.commit()
    print(f'User {update.effective_user.id} set to default')

