from data import db_session
from data.character import Character
from data.items import Items

db_session.global_init("../rpg.db")
db_sess = db_session.create_session()

"""
item1 = Items(name="Меч кладенец", description="Лучший меч")
item2 = Items(name="Большой щит", description="Огромный!")
db_sess.add(item1)
db_sess.add(item2)
db_sess.commit()

"""
character = db_sess.query(Character).first()  # наш персонаж
item1 = db_sess.query(Items).filter(Items.id == 1).first()
item2 = db_sess.query(Items).filter(Items.id == 2).first()

character.inventory.append(item1)  # добавили персонажу в инвентарь item1
character.inventory.append(item2)  # добавили персонажу в инвентарь item2

print("После добавления")
for item in character.inventory:
    print(item.to_dict(only=['name', 'description']))
character.inventory.remove(item1)  # удалили item1
print("После удаления")
for item in character.inventory:
    print(item.to_dict(only=['name', 'description']))
