from .asset import Asset
from .character import Character
from .exceptions import PlayerExistsInCampaignError


class Campaign(Asset):

    name = "A Generic Campaign"

    def __init__(self):
        self.players = {}
        self.rooms = {}
        self.current_room = None
        self.adventurers = {}

    @property
    def header(self):
        return f"* {self.name} - {self.current_room.name} *"

    def add_character(self, name, race):
        if name in self.adventurers:
            raise PlayerExistsInCampaignError()
        new_char = Character(name=name, race=race)
        self.adventurers[name] = new_char
        self.current_room.add_character(new_char)
        return None
