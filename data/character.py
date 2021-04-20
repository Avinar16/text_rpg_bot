import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Character(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'character'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))  # внешний ключ на таблицу пользователей
    room_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("rooms.id"))  # внешний ключ на таблицу с комнатами
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)

    room = orm.relation('Rooms', backref="character")

    hp = sqlalchemy.Column(sqlalchemy.Integer, default=5)
    max_hp = sqlalchemy.Column(sqlalchemy.Integer, default=5)

    level = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    exp = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    armor = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    attack = sqlalchemy.Column(sqlalchemy.Integer, default=1)



