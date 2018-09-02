from game.adventure.campaign import Campaign
from game.adventure.room import Room
from game.adventure.item import Item
from game.adventure.character import Character


class DeepDungeon(Campaign):
    name = "The Deep Dungeon"

    def __init__(self):
        super().__init__()
        dank_cell = {
            'name': 'Dank Cell',
            'desc': 'You are in a small, dank cell.',
        }

        self.rooms = {
            'dank_cell': Room(**dank_cell)
        }

        self.current_room = self.rooms['dank_cell']

        self.current_room.add_character(Character(name='Blorgth', race='Kobold'))
        self.current_room.add_character(Character(name='Spadge', race='Kobold'))
        self.current_room.add_character(Character(name='John', race='Accountant'))
        self.current_room.inventory = [
            Item('dirty sheet')
        ]

