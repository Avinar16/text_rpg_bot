from data import db_session
from functions.service_funcs.get_data import get_data_user, get_data_character
from data.inventory import Inventory
from data.items import Items


def inventory(update, context):
    db_sess = db_session.create_session()
    cur_char = get_data_character(update)
    inventory = db_sess.query(Inventory).filter(Inventory.char_id == cur_char.id).all()
    result = 'Выберете предмет для взаимодействия'
    result_dict = {}
    for count, inv_obj in zip(range(1, len(inventory) + 1), inventory):
        item = db_sess.query(Items).filter(Items.id == inv_obj.item_id).first()

        if inv_obj.is_equiped:
            result += f'{count}. - {item.name}, Надето'
        else:
            result += f'{count}. - {item.name}'
        # Словарь предметов и объекты инвентаря.
        result_dict[count] = [item, inv_obj]
    update.message.reply_text(result)
    return 4


def print_stats(update, context):
    current_char = get_data_character(update)
    update.message.reply_text(f'''
    HP - {current_char.hp}
Maximum hp - {current_char.max_hp}
Level - {current_char.level}
Exp - {current_char.exp}''', )
