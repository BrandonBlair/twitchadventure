from collections import Counter

from .exceptions import CharacterExistsInRoomError, CharacterNotInRoomError


class Room(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.inventory = []
        self.characters = {}

    @property
    def full_desc(self):
        return f"{self.desc} You see {self.roll_call}"

    def add_character(self, character):
        if character.name in self.characters:
            raise CharacterExistsInRoomError(f"{character.name} is already in {self.name}")
        self.characters[character.name] = character

    def remove_character(self, character):
        if character.name not in self.characters:
            raise CharacterNotInRoomError(f"{character.name} not in {self.name}")

    def attack(self, attacker, defender):
        pass

    def search(self, player):

        item_names = [
            itm.name for itm in self.inventory if itm.required_perception <= player.perception
        ]
        item_pairs = []
        ctr = Counter(item_names)
        for itm in ctr:
            total = ctr[itm]
            item_pairs.append(f"{total} {itm}{'s' if total > 1 else ''}")
        if len(item_pairs) == 1:
            joined = item_pairs[0]
        elif len(item_pairs) > 1:
            joined = ', '.join(item_pairs[:-1]) + f' and {item_pairs[-1]}.'
        else:
            joined = ''
        result = "doesn't find anything." if len(joined) == 0 else f"finds {joined}"
        msg = f"{player.name} searches the area and {result}"
        return msg

    @property
    def roll_call(self):
        roll = []
        races = [char.race for char in self.characters.values()]
        ctr = Counter(races)
        for race in ctr:
            total = ctr[race]
            roll.append(f"{total} {race}{'s' if total > 1 else ''}")
        if len(roll) == 1:
            joined = roll[0]
        elif len(roll) > 1:
            joined = ', '.join(roll[:-1]) + f' and {roll[-1]}.'
        else:
            joined = ''
        return joined



