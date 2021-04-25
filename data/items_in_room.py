import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Items_in_room(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'items_in_room'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    room_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('rooms.id'))

    item_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('items.id'))

    rooms = orm.relationship("Rooms", backref="items")
    items = orm.relationship("Items", backref="rooms")
