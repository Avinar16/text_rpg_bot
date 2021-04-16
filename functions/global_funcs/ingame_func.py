from data import db_session
from functions.service_funcs.get_data import get_data_user, get_data_character
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data.inventory import Inventory
from data.items import Items
from data.item_types import Item_types

# Стейты из ConversationHandler файла main
REGISTER, ENTER, EXIT, INVENTORY = range(1, 5)


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
            result += f'{count} - {item.name}'

        # Словарь предметов и объекты инвентаря.
        result_dict[count] = [item, inv_obj]
    # Запись словаря в глобальную user_data и вывод клавиатуры
    context.user_data['inventory'] = result_dict
    reply_keyboard = [['/back']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    # Вывод всех предметов из инвентаря
    update.message.reply_text(result, reply_markup=markup)
    return INVENTORY


# ДВЕ ФУНКЦИИ ИНВЕНТАРЯ НИЖЕ НУЖНО ВЫНЕСТИ В ОТДЕЛЬНЫЙ ФАЙЛ, АНДЕРСТЕНД?

def item_choose(update, context):
    count = update.message.text
    # команда возврата
    if count == '/back':
        return inv_back(update, context)

    # Выбор предмета для взаимодействия, определение выводимого текста
    if count.isdigit() and int(count) in context.user_data['inventory'].keys():
        # Получаем предмет из таблицы Items и Inventory которые были записаны ранее
        item, inv_obj = context.user_data['inventory'][int(count)]

        # Тип предмета для красивого отображения .name
        db_sess = db_session.create_session()
        item_type = db_sess.query(Item_types).filter(Item_types.id == item.item_type_id).first()

        # Вывод выбранного предмета и его описания
        result = f"Выбрано {item.name}, {item_type.name}, \n"
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
        result += '/drop - выкинуть'
        update.message.reply_text(result)


def inv_back(update, context):
    # Возвращение из инвентаря в комнату
    reply_keyboard = [['/West', '/North', '/East'],
                      ['/help']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Возвращаемся назад к комнате', reply_markup=markup)
    return EXIT


def print_stats(update, context):
    # Вывод статов(потом их будет больше)
    current_char = get_data_character(update)
    update.message.reply_text(f'''
    HP - {current_char.hp}
Maximum hp - {current_char.max_hp}
Level - {current_char.level}
Exp - {current_char.exp}''', )
