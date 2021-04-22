import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Rooms(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    base_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("room_list.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # тут можно добавить backref, если мы хотим знать, в каких комнатах находится конкретный моб в модели мобов,
    # например backref='rooms' создать у модели Mobs поле rooms, но вряд ли это подходит нам в данном случае.
    # аналогично
    items = orm.relation("Items",
                         secondary="items_in_room")
