from data import db_session
import random
from data.character import Character


def update_room(char):
    new_room_id = random.randrange(2, 11)
    char.room_id = new_room_id
    print(new_room_id)
