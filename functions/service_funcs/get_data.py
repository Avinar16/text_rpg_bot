from data.users import User
from data.mobs import Mobs
from data.character import Character
from data.room_list import Room_list
from data import db_session


def get_data_user(update, return_sess=False):
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    if return_sess:
        return current_user, db_sess
    return current_user


def get_data_character(update, return_sess=False):
    db_sess = db_session.create_session()
    current_char = db_sess.query(Character).filter(Character.user_id == update.effective_user.id,
                                                   Character.is_alive).first()
    if return_sess:
        return current_char, db_sess
    return current_char


def get_data_rooms(id):
    db_sess = db_session.create_session()
    current_room = db_sess.query(Room_list).filter(Room_list.id == id).first()
    return current_room


def get_mobs_in_room(id, return_sess=False):
    db_sess = db_session.create_session()
    current_mobs = db_sess.query(Mobs).filter(Mobs.room_id == id).all()
    if return_sess:
        return current_mobs, db_sess
    return current_mobs
