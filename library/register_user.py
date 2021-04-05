from data.users import User
import sqlalchemy.exc


def register(db_sess, update):
    try:
        db_sess = db_sess.create_session()
        user = User(
            tg_id=update.effective_user.id,
            score=0,
            best_score=0,
            in_game=False)
        db_sess.add(user)
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        print("User's already exist " + str(update.effective_user.id))

