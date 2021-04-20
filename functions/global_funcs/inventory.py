from data import db_session
from telegram import ReplyKeyboardMarkup
from data.inventory import Inventory
from data.item_types import Item_types
from .ingame_func import inventory
from .item_interactions import *
from functions.service_funcs.inv_back import inv_back

REGISTER, ENTER, EXIT, INVENTORY, ITEM_INTERACTION, END_GAME = range(1, 7)


# ////////////////////////////////
# нужно добавить учет характеристик
# ////////////////////////////////

def item_choose(update, context):
    count = update.message.text
    # команда возврата
    if count == '/back':
        return inv_back(update, context, EXIT)

    # Выбор предмета для взаимодействия, определение выводимого текста
    if count.isdigit() and int(count) in context.user_data['inventory'].keys():
        # Получаем предмет из таблицы Items и Inventory которые были записаны ранее
        item, inv_obj = context.user_data['inventory'][int(count)]

        # Тип предмета для красивого отображения .name
        db_sess = db_session.create_session()
        item_type = db_sess.query(Item_types).filter(Item_types.id == item.item_type_id).first()

        # Вывод выбранного предмета и его описания
        result = f"{item.name}, {item_type.name}, \n"
        result += f'{item.description} \n'

        # Надето ли?
        if inv_obj.is_equiped:
            result += f'Надето \n'
        # Если предмет можно надеть
        if int(item.item_type_id) == 1 or int(item.item_type_id) == 2:
            result += '/equip - надеть/снять \n'
        # Если предмет можно использовать
        else:
            result += '/use - использовать \n'
        # /drop, работает для всех предметов
        result += '/drop - выкинуть'
        update.message.reply_text(result)
        # Добавляем выбраный предмет в user_data для дальнейшей обработки
        context.user_data['current_item'] = [item, inv_obj]
        # стейт взаимодействия с предметом
        return ITEM_INTERACTION
    else:
        update.message.reply_text('Предмет не найден, введите правильное значение')
        return inv_back(update, context, INVENTORY)


def item_interaction(update, context):
    text = update.message.text
    item, inv_obj = context.user_data['current_item']

    if text == '/back':
        pass
    # Выкинуть предмет
    elif text == '/drop':
        drop(update, context, item, inv_obj)
        update.message.reply_text('Предмет волшебным образом растворился у вас в руках')
        # Вернуться в инвентарь
    elif item.item_type_id == 1 or item.item_type_id == 2:
        if text == '/equip':
            equip(update, context, item, inv_obj)
    elif item.item_type_id == 3:
        if text == '/use':
            use(update, context, item, inv_obj)
    return inv_back(update, context, INVENTORY)
