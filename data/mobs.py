import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Mobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mobs'

    hp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mobs_list.hp'))

    # armor = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mobs_list.armor'))
    attack = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('mobs_list.attack'))

    room_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('rooms.id'), primary_key=True)

    mob_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey('mobs_list.id'), primary_key=True)

    rooms = orm.relationship("Rooms", backref="mobs")
    mobs = orm.relationship("Mobs_list", backref="rooms")
