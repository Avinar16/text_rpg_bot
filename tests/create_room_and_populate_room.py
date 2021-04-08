from data import db_session
from data.character import Character
from data.items import Items
from data.rooms import Rooms
from data.mobs import Mobs

"""
Создадим монстров, комнату, наполним ее, привяжем к ней персонажа
"""
db_session.global_init("../rpg.db")
db_sess = db_session.create_session()

character = db_sess.query(Character).first()  # наш персонаж
"""
# создание монстров
mob1 = Mobs(name="Клыкастый златогрив")
mob2 = Mobs(name="Безобидная мышь")
db_sess.add(mob1)
db_sess.add(mob2)

# создание комнаты
room1 = Rooms(description="Ужасно прекрасная комната")
db_sess.add(room1)
db_sess.commit()
print(room1.id)

# наполнение комнаты монстрами и предметами

item1 = db_sess.query(Items).filter(Items.name == "Меч кладенец").first()
mob1 = db_sess.query(Mobs).filter(Mobs.name == "Безобидная мышь").first()
room1 = db_sess.query(Rooms).first()
 room1.items.append(item1)  # добавили в комнату меч
 room1.mobs.append(mob1) # добавили в комнату монстра
for item in room1.items:
    print(item.to_dict(only=["name"]))
for mob in room1.mobs:
    print(mob.to_dict(only=["name"]))
"""
room1 = db_sess.query(Rooms).first()

character.room = room1
db_sess.commit()
for mob in character.room.mobs:
    print(mob.to_dict(only=["name"]))