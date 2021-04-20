from data.users import User
from data.items import Items
from data.keyboards import exit_room_keyboard
from functions.service_funcs.get_data import get_data_rooms
from data.character import Character
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data.inventory import Inventory
from data import db_session
from functions.User_Character import User_Interaction_with_Character
from functions.debug_func.char_defaut import char_default


def register_user(update):
    user_info = update.effective_user
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.tg_id == update.effective_user.id).first():
        user = User(
            tg_id=update.effective_user.id,
            score=0,
            best_score=0,
            in_game=False)
        db_sess.add(user)
        db_sess.commit()
    update.message.reply_text(f'Добро пожаловать в EndlessDungeon, {user_info["first_name"]}!')


def register_char(update, context):
    db_sess = db_session.create_session()
    user_info = update.effective_user
    if not db_sess.query(Character).filter(Character.user_id == update.effective_user.id).first():
        user_character = Character(
            user_id=user_info.id,
            room_id=1,
            name=update.message.text,
            hp=5,
            max_hp=5,
            level=1,
            exp=0,
            armor=1,
            attack=3)
        db_sess.add(user_character)

        start_sword = db_sess.query(Items).filter(Items.id == 1).first()
        add_sword = Inventory(is_equiped=True)
        add_sword.items = start_sword
        add_sword.character = user_character
        db_sess.add(add_sword)
        db_sess.commit()
    reply_keyboard = exit_room_keyboard
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(f'Персонаж создан, его имя -  {update.message.text}',
                              reply_markup=markup)
    User_Interaction_with_Character(update, context)
    user_room = get_data_rooms(1)
    update.message.reply_text(f' Вы находитесь в: {user_room.name} \n{user_room.description}')
    return 3
