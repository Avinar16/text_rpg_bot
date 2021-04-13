import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm

# формируем связь многие ко многим к персонажам через промежуточную таблицу inventory


items_in_room = sqlalchemy.Table(
    'items_in_room',  # название промежуточной таблицы в базе
    SqlAlchemyBase.metadata,
    # что с чем связываем - rooms.id с
    sqlalchemy.Column('room_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('rooms.id')),
    # items.id
    sqlalchemy.Column('item_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('items.id'))
)


class Items(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    item_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('item_types.id'))


class Inventory(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'inventory'
    # что с чем связываем - character.id с
    char_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('character.id'), primary_key=True)
    # items.id
    item_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('items.id'), primary_key=True)
    is_equiped = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    items = orm.relationship("Items", backref="characters")
    character = orm.relationship("Character", backref="inventory")
