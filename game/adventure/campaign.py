from .asset import Asset
from .character import Character
from .exceptions import PlayerExistsInCampaignError


class Campaign(Asset):

    name = "A Generic Campaign"

    def __init__(self, console):
        self.console = console
        self.players = {}
        self.rooms = {}
        self.current_room = None
        self.adventurers = {}

    @property
    def header(self):
        return f"* {self.name} - {self.current_room.name} *"

    def add_character(self, console, name, race):
        if name in self.adventurers:
            raise PlayerExistsInCampaignError()
        new_char = Character(console=console, name=name, race=race, is_player=True)
        self.adventurers[name] = new_char
        self.current_room.add_character(new_char)
        return None
