import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Items(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    item_type_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('item_types.id'))

    attack_armor = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    level = sqlalchemy.Column(sqlalchemy.Integer, default=1)
