import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Mobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    room_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('rooms.id'))

    mob_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey('mobs_list.id'))

    rooms = orm.relationship("Rooms", backref="mobs")
    mobs = orm.relationship("Mobs_list", backref="rooms")

    hp = sqlalchemy.Column(sqlalchemy.Integer)

    armor = sqlalchemy.Column(sqlalchemy.Integer)
    attack = sqlalchemy.Column(sqlalchemy.Integer)
