from data import db_session
from data.users import User
from data.character import Character


db_session.global_init("../rpg.db")
db_sess = db_session.create_session()
"""
user = User(
    tg_id=random.randrange(10900000),
    score=0,
    best_score=5,
    in_game=True
)
db_sess.add(user)
db_sess.commit()
"""
"""
user = db_sess.query(User).first() # наш юзер с уже заполненным id

character = Character(user_id=user.id,
                      name="Перс",
                      )
db_sess.add(character)
db_sess.commit()
"""
user = db_sess.query(User).first()  # наш юзер с уже заполненным id

character = Character(user_id=user.id,
                      name="Перс",
                      )
db_sess.add(character)
db_sess.commit()

character = db_sess.query(Character).first()  # наш персонаж

print(character.user.to_dict(only=['id', 'tg_id', 'score']))  # проверяем что связь доступна

user = db_sess.query(User).first()
print(user.character.to_dict(only=['id', 'name']))  # проверяем что связь доступна
