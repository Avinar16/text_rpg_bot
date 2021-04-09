import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin



class Room_list(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'room_list'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    # тут можно добавить backref, если мы хотим знать, в каких комнатах находится конкретный моб в модели мобов,
    # например backref='rooms' создать у модели Mobs поле rooms, но вряд ли это подходит нам в данном случае.
    # mobs = orm.relation("Mobs",
    #                    secondary="mobs_in_room")
    # аналогично
    # items = orm.relation("Items",
    #                    secondary="items_in_room")
