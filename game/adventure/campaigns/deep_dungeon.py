from game.adventure.campaign import Campaign
from game.adventure.room import Room
from game.adventure.item import Item
from game.adventure.character import Character


class DeepDungeon(Campaign):
    name = "The Deep Dungeon"

    def __init__(self, console):
        super().__init__(console)
        dank_cell = {
            'name': 'Dank Cell',
            'desc': 'You are in a small, dank cell.',
        }

        self.rooms = {
            'dank_cell': Room(self.console, **dank_cell)
        }

        self.current_room = self.rooms['dank_cell']

        self.current_room.add_character(Character(self.console, name='Blorgth', race='Kobold', agility=6, max_health=35))
        self.current_room.add_character(Character(self.console, name='Spadge', race='Kobold', agility=8, max_health=26))
        self.current_room.add_character(Character(self.console, name='John', race='Accountant', agility=4, max_health=20))
        self.current_room.inventory = [
            Item('dirty sheet'),
            Item('badass sword', category='weapon', strength=10),
            Item('awesome flail', category='weapon', strength=4),
        ]

