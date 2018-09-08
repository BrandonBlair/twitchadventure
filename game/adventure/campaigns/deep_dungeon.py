from game.adventure.campaign import Campaign
from game.adventure.room import Room
from game.adventure.item import Item
from game.adventure.character import Character
from game.adventure.generators.rooms import random_room


class DeepDungeon(Campaign):
    name = "The Deep Dungeon"

    def __init__(self, console):
        super().__init__(console)
        self.rooms = {}
        self.current_room = None
        self.next_room()

    def next_room(self):
        procedurally_generated_room = random_room(self.console)
        room_name = procedurally_generated_room.name
        self.rooms[room_name] = procedurally_generated_room
        self.current_room = self.rooms[room_name]
        return None
