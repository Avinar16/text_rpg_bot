from data import db_session
from data.users import User
import sqlalchemy.exc


def Game(update):
    db_sess = db_session.create_session()
    current_user = db_sess.query(User).filter(User.tg_id == update.effective_user.id).first()
    if not current_user.in_game:
        update_db()

def update_db():
    sqlalchemy.update(User.in_game, True)