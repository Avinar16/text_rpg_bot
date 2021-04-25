from data.states import *
from functions.service_funcs.get_data import get_data_character
from data.mobs_list import Mobs_list
from data.keyboards import fight_keyboard
from telegram import ReplyKeyboardMarkup


def enemy_choose(update, context):
    count = update.message.text
    if count == '/back':
        return start_fight(update, context)
    # если введенный индекс в списке существующих мобов
    if count.isdigit() and int(count) in context.user_data['mobs_in_fight'].keys():
        # переменная для вывода текста
        # моб и информация о нем
        mob, mob_info = context.user_data['mobs_in_fight'][int(count)]
        result = f"""{mob_info.name}, {mob_info.level} уровня
{mob_info.description}

HP - {mob.hp} / {mob_info.max_hp}
Атака - {mob_info.attack}
Защита - {mob_info.armor}
Опыта падает - {mob_info.exp_drop}

/back - вернуться к списку врагов"""
        # нужно вернуть клаву
        update.message.reply_text(result)
    else:
        update.message.reply_text('Враг не найден, введите правильное значение')
        return ENEMY_CHOOSE


def enemy_interaction(update, context):
    pass


def start_fight(update, context):
    char, db_sess = get_data_character(update, return_sess=True)
    room = char.room
    if room.mobs:
        # Через первого моба в комнате будем узнавать чей первый ход
        mob_fromlist = db_sess.query(Mobs_list).filter(Mobs_list.id == room.mobs[0].mob_id).first()
        # Начало строки вывода, описание комнаты
        result = f'Вы пришли в {room.name} \n{room.description}\n'
        # Определение первого хода
        # если первый моб из всех <= уровнем чем игрок, то первый ход - игрока
        if mob_fromlist.level <= char.level:
            result += 'В комнате враги!\nВы ходите первым, выберите врага для удара\n'
        # если mob.lvl > char.lvl, первый ход- врагов
        else:
            result += 'В комнате враги!\nХод врага.\n'
            # hit
        result_dict = {}
        for count, mob in zip(range(1, len(room.mobs) + 1), room.mobs):
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
        # Выбор моба
        return ENEMY_CHOOSE
    else:
        update.message.reply_text(f'Вы пришли в {room.name} \n{room.description}\n')
        return EXIT
