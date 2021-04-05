import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)
    best_score = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)
    in_game = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    # сформировали обратную связь на модель персонажей
    # чтобы мы могли достать персонажа через user.character
    character = orm.relation("Character", backref='user', uselist=False)
    # back_populates - указываем на то поле, через которое мы связаны в модели Character
    # uselist = false - указываем, если у нас связь один к одному - каждому пользователю принадлежит только 1 персонаж
    # нужно, чтобы не писать user.character[0], а писать просто user.character
