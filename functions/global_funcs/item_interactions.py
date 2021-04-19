from data import db_session
from data.inventory import Inventory
from functions.service_funcs.inv_back import inv_back
from functions.service_funcs.get_data import get_data_character

REGISTER, ENTER, EXIT, INVENTORY, ITEM_INTERACTION, END_GAME = range(1, 7)


def drop(id):
    db_sess = db_session.create_session()
    inventory_item = db_sess.query(Inventory).filter(Inventory.item_id == id).first()
    db_sess.delete(inventory_item)
    db_sess.commit()


# ////////////////////////////////
# нужно добавить учет характеристик
# ////////////////////////////////

def equip(update, context, items, inv_obj):
    db_sess = db_session.create_session()
    # Определение сколько предметов надето
    current_char = get_data_character(update)
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
    # equip
    else:
        # Если оружие
        if fr_inv_obj.items.item_type_id == 1 and equiped_weapon < MAX_EQUIPED_WEAPON:
            fr_inv_obj.is_equiped = True
            update.message.reply_text(f'Оружие "{fr_inv_obj.items.name}" надето')
        # Если броня
        elif fr_inv_obj.items.item_type_id == 2 and equiped_armor < MAX_EQUIPED_ARMOR:
            fr_inv_obj.is_equiped = True
            update.message.reply_text(f'Броня "{fr_inv_obj.items.name}" надета')
        # Если превышен лимит
        elif equiped_weapon >= MAX_EQUIPED_WEAPON or equiped_armor >= MAX_EQUIPED_ARMOR:
            update.message.reply_text(f"""Надето слишком много предметов одного типа \n
Максимум брони - {MAX_EQUIPED_ARMOR}
Максимум оружия - {MAX_EQUIPED_WEAPON}""")
    db_sess.commit()


# in dev
# ////////////////////////////////
# нужно добавить учет эффектов
# ////////////////////////////////

def use(update, context, item, inv_obj):
    update.message.reply_text(f'Предмет {item.name} использован ( но это не точно )')
