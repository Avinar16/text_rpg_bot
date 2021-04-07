from data.users import User


def user_default(update, db_session):
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    current_user.in_game = False
    current_user.score = 0
    current_user.best_score = 0
    db_sess.commit()
    print(f'User {update.effective_user.id} set to default')
