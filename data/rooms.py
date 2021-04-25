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
