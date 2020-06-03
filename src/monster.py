from room import Room
import random


class Monster:
    def __init__(self, name: str, room: Room, strength: int = 50):
        self.name = name
        self.room = room
        self.strength = strength

    def change_room(self, room: Room):
        self.room = room

    def attack(self):
        return int(self.strength * (random.randint(1, 100)/100))
