from data import db_session
from functions.service_funcs.get_data import get_data_character
from telegram import ReplyKeyboardMarkup
from data.inventory import Inventory
from data.items import Items
from telegram.ext import ConversationHandler
from functions.debug_func.char_defaut import char_default
from data.keyboards import inv_keyboard
from data.users import User

# Стейты из ConversationHandler файла main
REGISTER, ENTER, EXIT, INVENTORY, ITEM_INTERACTION, END_GAME = range(1, 7)
from functions.service_funcs.get_data import get_data_rooms
from functions.service_funcs.Updater_db_file import update_room
from functions.service_funcs.get_data import get_data_character


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
    # Вывод статов(потом их будет больше)
    current_char = get_data_character(update)
    update.message.reply_text(f'''
Персонаж {current_char.name}
HP - {current_char.hp}
Maximum hp - {current_char.max_hp}
Level - {current_char.level}
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
    user = get_data_character(update)
    update_room(update, user.room_id, user.user_id)
    user_room = get_data_rooms(user.room_id)
    update.message.reply_text(f'Вы пришли в {user_room.name} \n{user_room.description}')



def fight(update, context):
    pass


def protection(update, context):
    pass
