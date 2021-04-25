from data.states import *


def enemy_choose(update, context):
    count = update.message.text

    if count.isdigit() and int(count) in context.user_data['mobs_in_fight'].keys():
        return ENEMY_INTERACTION
    else:
        update.message.reply_text('Враг не найден, введите правильное значение')
        return ENEMY_CHOOSE


def enemy_interaction(update, context):
    pass