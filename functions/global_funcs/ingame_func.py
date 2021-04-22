from data import db_session
from telegram import ReplyKeyboardMarkup
from data.inventory import Inventory
from data.items import Items
from telegram.ext import ConversationHandler
from functions.debug_func.char_defaut import char_default
from data.keyboards import inv_keyboard
from data.users import User
from functions.service_funcs.get_data import get_data_rooms
from functions.global_funcs.room_funcs import *
from functions.service_funcs.Updater_db_file import create_room
from functions.service_funcs.get_data import *
import random

# Стейты из ConversationHandler файла main
REGISTER, ENTER, EXIT, INVENTORY, ITEM_INTERACTION, END_GAME = range(1, 7)


def inventory(update, context):
    db_sess = db_session.create_session()
    cur_char = get_data_character(update)
    inventory = db_sess.query(Inventory).filter(Inventory.char_id == cur_char.id).all()

    # Строка для вывода пользователю
    result = 'Выберете предмет для взаимодействия \n'

    # Словарь, по сути и будет инвентарем
    result_dict = {}
    # Порядковый номер предмета и объект предмета из Inventory
    for count, inv_obj in zip(range(1, len(inventory) + 1), inventory):
        # Объект предмета из таблицы Items
        item = db_sess.query(Items).filter(Items.id == inv_obj.item_id).first()

        # Красивое отображение
        if inv_obj.is_equiped:
            result += f'{count} - {item.name}, Надето \n'
        else:
            result += f'{count} - {item.name} \n'

        # Словарь предметов и объекты инвентаря.
        result_dict[count] = [item, inv_obj]
    # Запись словаря в глобальную user_data и вывод клавиатуры
    context.user_data['inventory'] = result_dict
    reply_keyboard = inv_keyboard
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    # Вывод всех предметов из инвентаря
    update.message.reply_text(result, reply_markup=markup)
    return INVENTORY


def print_stats(update, context):
    # Вывод статов
    current_char = get_data_character(update)
    update.message.reply_text(f'''
Персонаж {current_char.name}, {current_char.level}lvl
HP - {current_char.hp} / {current_char.max_hp}
Attack - {current_char.attack}
Armor - {current_char.armor}
Exp - {current_char.exp}''', )


# Прерывание игры
def end_game(update, context):
    db_sess = db_session.create_session()
    char_default(update)
    user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    user.in_game = False
    db_sess.commit()
    update.message.reply_text('Игра завершена. Начать новую игру - /start')
    return ConversationHandler.END


def move_between_rooms(update, context):
    room = create_room(update, context)
    update.message.reply_text(f'Вы пришли в {room.name} \n{room.description}')
    return ENTER


def fight(update, context):
    cur_char = get_data_character(update)
    mobs, db_sess = get_mobs_in_room(cur_char.room_id, return_sess=True)
    damage = cur_char.attack
    mob = mobs[0]
    new_mob_hp = int(mob.hp) - int(damage)
    setattr(mob, 'hp', str(new_mob_hp))
    db_sess.commit()
    Mob_model = db_sess.query(Mobs_list).filter(Mobs_list.id == mob.mob_id).first()
    update.message.reply_text(f'Вы нанесли {Mob_model.name}, {damage} урона')
    if int(mob.hp) == 0 or int(mob.hp) < 0:
        db_sess.delete(mob)
        update.message.reply_text(f'{Mob_model.name} повержен!')
        db_sess.commit()
        return EXIT
    get_hurt(update, context)
    return ENTER



def get_hurt(update, context):
    cur_char, db_sess = get_data_character(update, return_sess=True)
    mobs = get_mobs_in_room(cur_char.room_id)
    mob = mobs[0]
    damage = mob.attack
    new_char_hp = int(cur_char.hp) - int(damage)
    setattr(cur_char, 'hp', str(new_char_hp))
    db_sess.commit()
    Mob_model = db_sess.query(Mobs_list).filter(Mobs_list.id == mob.mob_id).first()
    update.message.reply_text(f'{Mob_model.name} нанёс вам {damage} урона')
    if int(cur_char.hp) == 0 or int(cur_char.hp) < 0:
        update.message.reply_text(f'{cur_char.name} погиб!')
        end_game(update, context)



def enter_room(update, context):
    cur_char = get_data_character(update)
    use_attack = update.message.text
    print(use_attack)
    add_items(update, context)
    if not len(get_mobs_in_room(cur_char.room_id)):
        add_mobs(update, context, cur_char.room_id)
    if use_attack == '/attack':
        pass
    else:
        if len(get_mobs_in_room(cur_char.room_id)):
            update.message.reply_text(f'В комнате враги!')
            return ENTER
    if use_attack == '/attack' and len(get_mobs_in_room(cur_char.room_id)):
        mobs_in_room = get_mobs_in_room(cur_char.room_id)
        mob = mobs_in_room[0]
        while mob.hp != 0 or mob.hp > 0:
            fight(update, context)
    return EXIT
