from collections import Counter
import time

from .exceptions import (
    CharacterExistsInRoomError,
    CharacterNotInRoomError,
    ItemNotFoundError,
    InvalidTargetError,
)
from game.adventure.chat_tools import title_case
from game.adventure import dice


class Room(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.inventory = []
        self.characters = {}

    @property
    def full_desc(self):
        """Provides a full description of the room, including all characters currently present."""

        return f"{self.desc} You see {self.roll_call}"

    def add_character(self, character):
        """Adds a character to the current room."""

        if character.name in self.characters:
            raise CharacterExistsInRoomError(f"{character.name} is already in {self.name}")
        self.characters[character.name] = character

    def remove_character(self, character):
        """Removes a character from the current room.

        NOTE: Currently they cease to exist upon removal, which is probably bad.
        """

        if character.name not in self.characters:
            raise CharacterNotInRoomError(f"{character.name} not in {self.name}")

        del self.characters[character.name]

    def attack(self, console, attacker, target_name):
        """Attempts an attack by one character of another."""

        target_name = target_name.lower()
        matching_targets = [
            trg for trg in self.characters.values() \
            if not trg.is_player \
            and trg.alive \
            and (target_name in trg.name.lower() or target_name in trg.race.lower())
        ]
        if len(matching_targets) == 0:
            raise InvalidTargetError(f"{target_name} is not a valid target.")
        defender = matching_targets[0]  # Best guess at name matching multiple targets

        # Roll for attack
        atk_roll = dice.roll_d20()
        console.chat(f"{attacker.name} rolls a D20 to attack. Result: {atk_roll}")

        # Handle a roll of 1
        if atk_roll == 1:
            console.chat("Rolling for critical fail...")
            crit_fail_roll = dice.roll_d20()
            if crit_fail_roll == 1:
                dmg = dice.roll_d6() + attacker.strength
                attacker.health -= dmg
                console.chat("Critical fail! You trip and impale yourself for {dmg} damage.")
                if attacker.health < 1:
                    attacker.alive = False
                    console.chat(f"{attacker.name} has been slain!")
            else:
                console.chat(
                    "You stumble, but regain your footing in time to try again next round."
                )
            return None

        # Handle anything else
        atk_score = attacker.agility + atk_roll
        console.chat(f"{attacker.name} swings...")
        defns = defender.defense
        if atk_score >= defender.defense:
            dmg_roll = dice.roll_d6()
            dmg_score = dmg_roll + attacker.damage
            console.chat(f"...and hits {defender.name} for {dmg_score} damage.")

            defender.health -= dmg_score
            if defender.health < 1:
                defender.alive = False
                console.chat(f"{defender.name} has been slain!")
            return None

        console.chat(f"...and misses!")
        return None


    def take(self, console, player, desired_item_name):
        """Attempts to take an item from the room and add it to a character's inventory."""

        desired_item_name = desired_item_name.lower()
        matching_items = sorted(
            [
                itm for itm in self.inventory if desired_item_name in itm.name.lower()
            ]
        )

        if len(matching_items) == 0:
            raise ItemNotFoundError(f'{desired_item_name} not found among {self.inventory}')
        chosen_item = matching_items[0]  # Choose first match, best effort.
        player.inventory.append(chosen_item)
        self.inventory.remove(chosen_item)
        console.chat(f"{player.name} takes {chosen_item.name}.")

    def drop(self, console, player, item_name):
        """Drops an item from a player's inventory and places it in the current room."""
        item = player.find_inventory_item_by_name(item_name)

        self.inventory.append(item)
        player.remove_item(obj=item)
        console.chat(f"{player.name} drops {item.name}")
        return None

    def search(self, player):
        """Attempts to find items in the current room using player's perception score."""

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
        """Displays all characters currently present in the room."""

        roll = []
        char_names_and_races = [(char.name, char.race, char.alive) for char in self.characters.values()]
        for name, race, alive in char_names_and_races:
            roll.append(f"{'the corpse of ' if not alive else ''}{title_case(name)} the {title_case(race)}")
        if len(roll) == 1:
            joined = roll[0]
        elif len(roll) > 1:
            joined = ', '.join(roll[:-1]) + f' and {roll[-1]}.'
        else:
            joined = ''
        return joined
