from data.item_types import Item_types
from .item_interactions import *
from functions.service_funcs.inv_back import inv_back
from data.states import *


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
        if item.item_type_id == 1:
            result += f'Атака: {item.attack_armor}\n'
        elif item.item_type_id == 2:
            result += f'Защита: {item.attack_armor}\n'
        # Надето ли?
        if inv_obj.is_equiped:
            result += f'Надето \n'
        # Если предмет можно надеть
        if int(item.item_type_id) == 1 or int(item.item_type_id) == 2 or item.item_type_id == 4 \
                or item.item_type_id == 5 or item.item_type_id == 6 :
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
    elif item.item_type_id == 1 or item.item_type_id == 2 or item.item_type_id == 4 or item.item_type_id == 5 \
            or item.item_type_id == 6 :
        if text == '/equip':
            equip(update, context, item, inv_obj)
    elif item.item_type_id == 3:
        if text == '/use':
            use(update, context, item, inv_obj)
    return inv_back(update, context, INVENTORY)
