from functions.service_funcs.get_data import get_data_user, get_data_character


def levelup_check(update, context):
    char, db_sess = get_data_character(update, return_sess=True)
    if char.level == 1:
        exp_need_to_lvlup = 1
    else:
        exp_need_to_lvlup = 10 * (char.level * 0.5) * (char.level // 2)
    if char.exp // exp_need_to_lvlup > 0:
        char.level += 1
        char.exp -= exp_need_to_lvlup
    db_sess.commit()


def record_check(update, context):
    user, db_sess = get_data_user(update, return_sess=True)
    # set up record
    user.score += 1
    if user.best_score < user.score:
        user.best_score = user.score
    db_sess.commit()
