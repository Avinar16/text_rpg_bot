from telegram import ReplyKeyboardMarkup
from data.states import *
from data.keyboards import inv_keyboard
from functions.service_funcs.create_room import *
from data.inventory import Inventory
from functions.service_funcs.get_data import *

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