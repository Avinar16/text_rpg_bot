from data import db_session
from data.inventory import Inventory
from functions.service_funcs.get_data import get_data_character
from functions.service_funcs.item_usages import item_usages


def drop(update, context, items, inv_obj):
    db_sess = db_session.create_session()
    char = get_data_character(update)

    inventory_item = db_sess.query(Inventory).filter(Inventory.item_id == items.id).first()
    fr_inv_obj = db_sess.query(Inventory).filter(Inventory.char_id == inv_obj.char_id,
                                                 Inventory.item_id == inv_obj.item_id).first()

    update.message.reply_text(f'Вы выкинули {fr_inv_obj.items.name}')

    if fr_inv_obj.is_equiped:
        if fr_inv_obj.items.item_type_id == 1:
            char.attack -= fr_inv_obj.items.attack_armor
        elif fr_inv_obj.items.item_type_id == 2:
            char.armor -= fr_inv_obj.items.attack_armor
        fr_inv_obj.is_equiped = False

    db_sess.delete(inventory_item)
    db_sess.commit()


def equip(update, context, items, inv_obj):
    current_char, db_sess = get_data_character(update, return_sess=True)
    # Определение сколько предметов надето
    equiped_armor = 0
    equiped_weapon = 0
    for item in current_char.inventory:
        if item.items.item_type_id == 1 and item.is_equiped:
            equiped_weapon += 1
        elif item.items.item_type_id == 2 and item.is_equiped:
            equiped_armor += 1

    # максимум надетых предметов
    MAX_EQUIPED_ARMOR = 3
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

    # equip
    else:
        # Если оружие
        if fr_inv_obj.items.item_type_id == 1 and equiped_weapon < MAX_EQUIPED_WEAPON:
            fr_inv_obj.is_equiped = True

            current_char.attack += fr_inv_obj.items.attack_armor

            update.message.reply_text(f'Оружие "{fr_inv_obj.items.name}" надето')
        # Если броня
        elif fr_inv_obj.items.item_type_id == 2 and equiped_armor < MAX_EQUIPED_ARMOR:
            fr_inv_obj.is_equiped = True

            current_char.armor += fr_inv_obj.items.attack_armor

            update.message.reply_text(f'Броня "{fr_inv_obj.items.name}" надета')
        # Если превышен лимит
        elif equiped_weapon >= MAX_EQUIPED_WEAPON or equiped_armor >= MAX_EQUIPED_ARMOR:
            update.message.reply_text(f"""Надето слишком много предметов одного типа \n
Максимум брони - {MAX_EQUIPED_ARMOR}
Максимум оружия - {MAX_EQUIPED_WEAPON}""")
    db_sess.commit()
    print('commit')


def use(update, context, item, inv_obj):
    update.message.reply_text(f'Предмет {item.name} использован')
    item_usages(update, context, item)
    drop(update, context, item, inv_obj)
