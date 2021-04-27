from ..service_funcs.get_data import get_data_character
from data import db_session
from data.items import Items
from data.states import *
from telegram import ReplyKeyboardMarkup
from data.keyboards import *
from data.room_list import Room_list
from data.inventory import Inventory
from data.item_types import Item_types
from .ingame_function.in_game_inv import inventory


def loot_handler(update, context):
    char = get_data_character(update)
    db_sess = db_session.create_session()
    if char.room.items:
        result_dict = {}
        result = 'Вам удалось найти...\n'
        for count, item_in_room in zip(range(1, len(char.room.items) + 1), char.room.items):
            item = db_sess.query(Items).filter(Items.id == item_in_room.item_id).first()

            # добавление словаря для поиска по числу
            result_dict[count] = (item, item_in_room)
            # Добавление текста
            result += f'{count} - {item.name}, {item.level}lvl\n'
        context.user_data['items_in_room'] = result_dict
        result += 'Выберите предмет для взаимодействия\n'
        reply_keyboard = loot_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text(result, reply_markup=markup)
        return LOOT_CHOOSE
    else:
        reply_keyboard = exit_room_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        update.message.reply_text('В комнате ничего не нашлось.', reply_markup=markup)
        return EXIT


def loot_choose(update, context):
    count = update.message.text

    # команда пропуска фазы лута
    if count == '/skip':
        db_sess = db_session.create_session()
        char = get_data_character(update)

        # Вывод клавиатуры
        reply_keyboard = exit_room_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text('Вы решили отставить поиски предметов', reply_markup=markup)
        # Информация для вывода комнаты
        room_info = db_sess.query(Room_list).filter(Room_list.id == char.room.base_id).first()
        update.message.reply_text(f'{room_info.name}\n{room_info.description}')
        return EXIT

    elif count == '/inventory':
        return inventory(update, context)

    # Выбор предмета для взаимодействия, определение выводимого текста
    if count.isdigit() and int(count) in context.user_data['items_in_room'].keys():
        item, item_in_room = context.user_data['items_in_room'][int(count)]

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
        # Вывод возможных операций
        result += '/back - вернуться к списку\n'
        result += '/take - взять предмет\n'

        keyboard = inv_keyboard
        markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
        update.message.reply_text(result, reply_markup=markup)
        # Добавляем выбраный предмет в user_data для дальнейшей обработки
        context.user_data['loot_item'] = (item, item_in_room)
        # стейт взаимодействия с предметом
        return LOOT_INTERACTION


def loot_interaction(update, context):
    text = update.message.text
    item, item_in_room = context.user_data['loot_item']
    char = get_data_character(update)

    db_sess = db_session.create_session()
    # Назад к списку
    if text == '/back':
        pass
    # Взять предметь
    elif text == '/take':
        if_item_in_inv = db_sess.query(Inventory).filter(Inventory.char_id == char.id,
                                                         Inventory.item_id == item.id).all()
        items_in_inv = db_sess.query(Inventory).filter(Inventory.char_id == char.id).all()
        if len(if_item_in_inv) > 0:
            update.message.reply_text("""У вас уже есть такой предмет,
магическая сумка не предусматривает ношение одинаковых предметов.""")
        elif len(items_in_inv) < 10:
            add_item = Inventory(is_equiped=False)
            add_item.items = item
            add_item.character = char
            db_sess.add(add_item)
            char.room.items.remove(item_in_room)
            update.message.reply_text(f"Вы взяли {item.name}")
        db_sess.commit()
    else:
        update.message.reply_text("""В вашей сумке слишком много предметов. Максимум - 10""")
    return loot_handler(update, context)
