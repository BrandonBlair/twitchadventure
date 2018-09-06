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
    def __init__(self, console, name, desc):
        self.console = console
        self.name = name
        self.desc = desc
        self.inventory = []
        self.characters = {}
        self.aggros = {}
        self.actions = {}

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

    def attack(self, player, attacker, target):
        """Prepares an attack action and places it into the queue_action

        The defender's Character object is retrieved using its name, some checks are
        made to handle initiative and combat status, and the action is placed into the
        queue where it will be weighed against other initiatives for execution.
        """

        defender = self._get_living_char_from_name(target)

        # Set aggro
        if self.aggros.get(attacker) is None:
            self.aggros[attacker] = set()
        if len(self.aggros.get(attacker)) == 0:
            attacker.start_combat()
        if defender not in self.aggros.get(attacker):
            self.console.chat(f"{attacker.name} moves to attack {defender.name}.")
            self.aggros[attacker].add(defender)
            defender.roll_initiative()

        kw = {
            'attacker': attacker,
            'defender': defender,
        }
        self.queue_action(player, self._attack, f_kwargs=kw)
        return None

    def _attack(self, attacker, defender):
        """Attempts an attack by one character of another."""

        # Roll for attack
        atk_roll = dice.roll_d20()
        self.console.chat(f"{attacker.name} rolls a D20 to attack. Result: {atk_roll}")

        # Handle a roll of 1
        if atk_roll == 1:
            self.console.chat("Rolling for critical fail...")
            crit_fail_roll = dice.roll_d20()
            if crit_fail_roll == 1:
                dmg = dice.roll_d6() + attacker.strength
                attacker.health -= dmg
                self.console.chat("Critical fail! You trip and impale yourself for {dmg} damage.")
                if attacker.health < 1:
                    attacker.alive = False
                    self.console.chat(f"{attacker.name} has been slain!")
            else:
                self.console.chat(
                    f"{attacker.name} stumbles, but regains their footing in time to try again next round."
                )
            return None

        # Handle anything else
        atk_score = attacker.agility + atk_roll
        self.console.chat(f"{attacker.name} swings...")
        defns = defender.defense
        if atk_score >= defender.defense:
            dmg_roll = dice.roll_d6()
            dmg_score = dmg_roll + attacker.damage
            self.console.chat(f"...and hits {defender.name} for {dmg_score} damage.")

            defender.health -= dmg_score
            if defender.health < 1:
                defender.alive = False
                self.unaggro_character(defender)
                self.console.chat(f"{defender.name} has been slain!")

                if len(self.aggros[attacker]) == 0:
                    attacker.end_combat()

            return None

        self.console.chat(f"...and misses!")
        return None

    def take(self, player, desired_item_name):
        kw = {
            'player': player,
            'desired_item_name': desired_item_name,
        }
        self.queue_action(player, self._take, f_kwargs=kw)
        return None

    def _take(self, player, desired_item_name):
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
        self.console.chat(f"{player.name} takes {chosen_item.name}.")
        return None

    def drop(self, player, item_name):
        kw = {'item_name': item_name}
        self.queue_action(player, self._drop, f_kwargs=kw)
        return None

    def _drop(self, player, item_name):
        """Drops an item from a player's inventory and places it in the current room."""
        item = player.find_inventory_item_by_name(item_name)

        self.inventory.append(item)
        player.remove_item(obj=item)
        self.console.chat(f"{player.name} drops {item.name}")
        return None

    def search(self, player):
        kw = {'player': player}
        self.queue_action(player, self._search, f_kwargs=kw)
        return None

    def _search(self, player):
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
        self.console.chat(msg)
        return None

    def _get_living_char_from_name(self, name):
        target_name = name.lower()
        matching_targets = [
            trg for trg in self.characters.values() \
            if not trg.is_player \
            and trg.alive \
            and (target_name in trg.name.lower() or target_name in trg.race.lower())
        ]
        if len(matching_targets) == 0:
            raise InvalidTargetError(f"{target_name} is not a valid target.")
        charctr = matching_targets[0]  # Best guess at name matching multiple targets
        return charctr

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

    def unaggro_character(self, char):
        for player in self.aggros:
            self.aggros[player] -= {char}

    def queue_action(self, player, func, f_args=None, f_kwargs=None):
        """Queues an action, causing any actions for the designated player to be queued as well."""

        f_args = f_args or []
        f_kwargs = f_kwargs or {}

        # Queue player action
        if player not in self.actions:
            self.actions[player] = {}
        if player.initiative not in self.actions[player]:
            self.actions[player][player.initiative] = []
        self.actions[player][player.initiative].append(
            (func, f_args, f_kwargs)
        )

        # Queue opponent actions
        for opponent in self.aggros[player]:
            if opponent.initiative not in self.actions[player]:
                self.actions[player][opponent.initiative] = []
            kw = {
                'attacker': opponent,
                'defender': player,
            }
            self.actions[player][opponent.initiative].append(
                (self._attack, [], kw)
            )

        # Trigger ordered actions
        self.process_queued_actions(player)

    def process_queued_actions(self, player):
        actions_by_highest_initiative = sorted(
            self.actions[player],
            reverse=True
        )
        for initv_nbr in actions_by_highest_initiative:
            for func_tuple in self.actions[player][initv_nbr]:
                func, fargs, fkwargs = func_tuple
                func(*fargs, **fkwargs)  # Execute action
        self.actions[player] = {}

        # Check for end of combat
