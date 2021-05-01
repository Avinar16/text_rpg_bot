from data import db_session
from data.inventory import Inventory
from functions.service_funcs.get_data import get_data_character
from functions.service_funcs.item_usages import item_usages


def drop(update, context, items, inv_obj):
    db_sess = db_session.create_session()
    char = get_data_character(update)
    fr_inv_obj = db_sess.query(Inventory).filter(Inventory.char_id == inv_obj.char_id,
                                                 Inventory.item_id == inv_obj.item_id).first()

    update.message.reply_text(f'Вы выкинули {fr_inv_obj.items.name}')

    if fr_inv_obj.is_equiped:
        if fr_inv_obj.items.item_type_id == 1:
            char.attack -= fr_inv_obj.items.attack_armor
        elif fr_inv_obj.items.item_type_id == 2:
            char.armor -= fr_inv_obj.items.attack_armor
        fr_inv_obj.is_equiped = False

    db_sess.delete(fr_inv_obj)
    db_sess.commit()


def equip(update, context, items, inv_obj):
    current_char, db_sess = get_data_character(update, return_sess=True)
    # Определение сколько предметов надето
    equiped_weapon = 0
    #Шлем
    equiped_armor_h = 0
    #Нагрудник
    equiped_armor_b = 0
    #Поножи
    equiped_armor_g = 0
    #Для полных комплектов брони
    equiped_armor_full = 0
    for item in current_char.inventory:
        if item.items.item_type_id == 1 and item.is_equiped:
            equiped_weapon += 1
        elif item.items.item_type_id == 2 and item.is_equiped:
            equiped_armor_h += 1
        elif item.items.item_type_id == 4 and item.is_equiped:
            equiped_armor_b += 1
        elif item.items.item_type_id == 5 and item.is_equiped:
            equiped_armor_g += 1
        elif item.items.item_type_id == 6 and item.is_equiped:
            equiped_armor_full += 1

    # максимум надетых предметов
    MAX_EQUIPED_ARMOR_ALL = 3
    MAX_EQUIPED_ARMOR_I = 1
    MAX_EQUIPED_WEAPON = 2

    # т.к inv_obj относится к другой сессии, то может содержать только собственную информацию
    # и не подходит для изменения базы, fr_inv_obj = inv_obj, но текущей сессии
    fr_inv_obj = db_sess.query(Inventory).filter(Inventory.char_id == inv_obj.char_id,
                                                 Inventory.item_id == inv_obj.item_id).first()

    # unequip
    if fr_inv_obj.is_equiped:
        fr_inv_obj.is_equiped = False
        update.message.reply_text(f'Вы сняли {items.name}')

        if fr_inv_obj.items.item_type_id == 1:
            current_char.attack -= fr_inv_obj.items.attack_armor
        elif fr_inv_obj.items.item_type_id == 2:
            current_char.armor -= fr_inv_obj.items.attack_armor
        elif fr_inv_obj.items.item_type_id == 4:
            current_char.armor -= fr_inv_obj.items.attack_armor
        elif fr_inv_obj.items.item_type_id == 5:
            current_char.armor -= fr_inv_obj.items.attack_armor
        elif fr_inv_obj.items.item_type_id == 6:
            current_char.armor -= fr_inv_obj.items.attack_armor

    # equip
    else:
        # Если оружие
        if fr_inv_obj.items.item_type_id == 1 and equiped_weapon < MAX_EQUIPED_WEAPON:
            fr_inv_obj.is_equiped = True

            current_char.attack += fr_inv_obj.items.attack_armor

            update.message.reply_text(f'Оружие "{fr_inv_obj.items.name}" надето')
        # Если броня
        elif fr_inv_obj.items.item_type_id == 2 and equiped_armor_h < MAX_EQUIPED_ARMOR_I:
            fr_inv_obj.is_equiped = True
        elif fr_inv_obj.items.item_type_id == 4 and equiped_armor_b < MAX_EQUIPED_ARMOR_I:
            fr_inv_obj.is_equiped = True
        elif fr_inv_obj.items.item_type_id == 5 and equiped_armor_g < MAX_EQUIPED_ARMOR_I:
            fr_inv_obj.is_equiped = True

            current_char.armor += fr_inv_obj.items.attack_armor

            update.message.reply_text(f'Броня "{fr_inv_obj.items.name}" надета')
        # Если превышен лимит
        elif equiped_weapon >= MAX_EQUIPED_WEAPON or equiped_armor_h >= MAX_EQUIPED_ARMOR_I \
                or (equiped_armor_h + equiped_armor_b + equiped_armor_g) >= MAX_EQUIPED_ARMOR_ALL or \
                equiped_armor_full >= MAX_EQUIPED_ARMOR_I:
            update.message.reply_text(f"""Надето слишком много предметов одного типа \n
Максимум брони выбранного типа - {MAX_EQUIPED_ARMOR_I}
Максимум оружия - {MAX_EQUIPED_WEAPON}""")
    db_sess.commit()
    print('commit')


def use(update, context, item, inv_obj):
    update.message.reply_text(f'Предмет {item.name} использован')
    item_usages(update, context, item)
    drop(update, context, item, inv_obj)
