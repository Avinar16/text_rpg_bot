import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin



class Mobs_list(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mobs_list'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    hp = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    max_hp = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    exp_drop = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    armor = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    attack = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    level = sqlalchemy.Column(sqlalchemy.Integer, default=1)
