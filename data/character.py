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

    # в свойстве room у объекта Character будет объект из модели Rooms,
    # backref - в модели Rooms будет поле character, где будет соответствующий персонаж, который сейчас в комнате
    # инвентарь персонажа, связь многие ко многим с моделью Items через вспомогательную таблицу inventory
    # (Смотри файл items.py)
    inventory = orm.relation("Items",
                             secondary="inventory",
                             backref="items")
