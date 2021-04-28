import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Inventory(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'inventory'
    # что с чем связываем - character.id с
    char_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('character.id'), primary_key=True)
    # items.id
    item_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('items.id'), primary_key=True)

    items = orm.relationship("Items", backref="characters")
    character = orm.relationship("Character")

    is_equiped = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
