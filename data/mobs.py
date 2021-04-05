import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

mobs_in_room = sqlalchemy.Table(
    'mobs_in_room',  # название промежуточной таблицы в базе
    SqlAlchemyBase.metadata,
    # что с чем связываем - mobs.id с
    sqlalchemy.Column('mob_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('mobs.id')),
    # rooms.id
    sqlalchemy.Column('room_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('rooms.id'))
)


class Mobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'mobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    stats = sqlalchemy.Column(sqlalchemy.String, nullable=True)
