import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

# формируем связь многие ко многим к персонажам через промежуточную таблицу inventory

inventory = sqlalchemy.Table(
    'inventory',  # название промежуточной таблицы в базе
    SqlAlchemyBase.metadata,
    # что с чем связываем - character.id с
    sqlalchemy.Column('char_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('character.id')),
    # items.id
    sqlalchemy.Column('item_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('items.id')),

    sqlalchemy.Column('is_equiped', sqlalchemy.Boolean, default=False)
)
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
