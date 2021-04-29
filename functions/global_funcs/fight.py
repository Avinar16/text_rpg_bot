from data.states import *
from functions.service_funcs.get_data import get_data_character
from data.mobs_list import Mobs_list
from math import floor
from data.keyboards import *
from telegram import ReplyKeyboardMarkup
from data.character import Character
from data.mobs import Mobs
from data import db_session
import random
from .ingame_function.in_game_inv import inventory
from .ingame_function.end_game import end_game
from .loot import loot_handler


def enemy_choose(update, context):
    char = get_data_character(update)
    count = update.message.text
    if count == '/back':
        return fight_handler(update, context, True)
    elif count == '/inventory':
        return inventory(update, context)

    # если введенный индекс в списке существующих мобов
    if count.isdigit() and int(count) in context.user_data['mobs_in_fight'].keys():
        # переменная для вывода текста
        # моб и информация о нем
        mob, mob_info = context.user_data['mobs_in_fight'][int(count)]
        result = f"""{mob_info.name}, {mob_info.level} уровня
{mob_info.description}

HP: {mob.hp} / {mob_info.max_hp}
Атака: {mob_info.attack}
Защита: {mob_info.armor}
Опыта падает: {mob_info.exp_drop}

/back - вернуться к списку врагов
/attack - Атаковать"""
        # keyboard
        reply_keyboard = enemy_interaction_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        # current mob
        context.user_data['current_mob'] = (mob, mob_info)
        # message
        update.message.reply_text(result, reply_markup=markup)
        return ENEMY_INTERACTION
    else:
        update.message.reply_text('Враг не найден, введите правильное значение')
        return ENEMY_CHOOSE


# = player_turn
def enemy_interaction(update, context):
    text = update.message.text
    # Возвращаемся к списку мобов если /back
    if text == '/back':
        return fight_handler(update, context, True)
    elif text == '/attack':
        # Выбранный моб и его инфа
        mob, mob_info = context.user_data['current_mob']
        char, db_sess = get_data_character(update, return_sess=True)
        # наносим урон
        do_damage(update, context, char, mob)
        check_die(update, context, mob)

        return fight_handler(update, context, False)


def enemy_turn(update, context):
    char = get_data_character(update)
    for mob, mob_info in context.user_data['mobs_in_fight'].values():
        do_damage(update, context, mob, char)
        if int(char.hp) <= 0:
            return check_die(update, context, char)
    context.user_data['turn'] = True
    return ENEMY_CHOOSE


def do_damage(update, context, whose_attack, who_gets_damage):
    db_sess = db_session.create_session()
    armor = int(who_gets_damage.armor)
    # Вычисление кооэфицента поглощения брони(прям как в доте)))
    damage_absorption = ((0.06 * armor) / (1 + 0.06 * armor))
    damage_absorption = round(damage_absorption, 2)

    # Исход удара
    hit = random.randrange(1, 21)
    # Само вычисление атаки с учётом брони
    damage = int(whose_attack.attack) - (int(whose_attack.attack) * damage_absorption)
    result = ''
    if hit >= 19:
        damage *= 2
        result += 'Критическая атака! Урон увеличен в 2 раза\n'
    elif hit <= 4:
        damage = 0
        result += 'Промах!\n'

    # Округление в меьшую сторону для увеличения эффективности брони
    new_hp = str(floor(int(who_gets_damage.hp) - damage))
    setattr(who_gets_damage, 'hp', new_hp)
    db_sess.commit()

    if isinstance(whose_attack, Character):
        result += f'Вы нанесли {round(damage)}\nУ врага осталось {who_gets_damage.hp}hp\n'
    elif isinstance(whose_attack, Mobs):
        result += f'Вам нанесли {round(damage)} урона\nУ вас осталось {who_gets_damage.hp}hp\n'
    update.message.reply_text(result)


def check_die(update, context, target):
    char = get_data_character(update)
    # Елси хп 0 или меньше
    if int(target.hp) <= 0:
        # Если цель- герой
        if isinstance(target, Character):
            update.message.reply_text('Вы погибли!')
            # Закончить игру
            return end_game(update, context)
        elif isinstance(target, Mobs):
            db_sess = db_session.create_session()
            # информация о мобе, чтобы красиво вывести текст
            mob_info = db_sess.query(Mobs_list).filter(Mobs_list.id == target.mob_id).first()
            update.message.reply_text(f'{mob_info.name} убит! Вы получаете {mob_info.exp_drop} опыта!')
            # Передаем опыт герою
            char.exp += int(mob_info.exp_drop)
            # Удаляем убитого моба
            char.room.mobs.remove(target)
            db_sess.delete(target)
            db_sess.commit()


def fight_handler(update, context, turn):
    # при первом заходе в комнату
    context.user_data['turn'] = turn

    char, db_sess = get_data_character(update, return_sess=True)
    room = char.room
    if room.mobs:
        # Начало строки вывода, описание комнаты

        result = 'В комнате враги!\n'

        mobs = db_sess.query(Mobs).filter(Mobs.room_id == char.room.id).all()
        result_dict = {}
        for count, mob in zip(range(1, len(mobs) + 1), mobs):
            # добавление мобов в словарь
            mob_fromlist = db_sess.query(Mobs_list).filter(Mobs_list.id == mob.mob_id).first()
            result_dict[count] = (mob, mob_fromlist)

            # добавление текста для вывода
            result += f'{count}. - {mob_fromlist.name}, {mob_fromlist.level} уровня\n'
        context.user_data['mobs_in_fight'] = result_dict

        # init клавиатуры
        reply_keyboard = fight_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        # вывод текста, вывод новой клавиатуры
        update.message.reply_text(result, reply_markup=markup)

        if not context.user_data['turn']:
            return enemy_turn(update, context)
        else:
            return ENEMY_CHOOSE
    else:
        reply_keyboard = loot_keyboard
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'Вы пришли в {room.name} \n{room.description}\n', reply_markup=markup)
        return loot_handler(update, context)
