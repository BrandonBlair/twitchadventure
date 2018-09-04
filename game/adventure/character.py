from game.adventure.asset import Asset
from game.adventure.exceptions import (
    ItemNotFoundError,
    ItemNotEquippableError,
    ItemNotEquippedError,
)


class Character(Asset):

    def __init__(self, console, name, race, is_player=False, strength=1, max_health=100, gold=0, perception=1, agility=1, armor_class=1, alive=True):
        self.console = console
        self.name = name
        self.race = race
        self.is_player = is_player
        self.equippable_types = ['weapon', 'armor']

        self.strength = strength
        self.max_health = max_health
        self.health = self.max_health
        self.alive = alive
        self.agility = agility
        self.perception = perception

        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.gold = gold

    def add_gold(self, amount):
        self.gold += amount

    def remove_gold(self, amount):
        self.gold -= amount

    def give_item(self, item):
        self.inventory.append(item)

    def remove_item(self, name=None, obj=None):
        """Removes an item from the player's inventory and unequips it if necessary."""

        item = self._find_by_name_or_obj(name, obj)
        if item.category in self.equippable_types and (self.equipped_armor == item or self.equipped_weapon == item):
            self.unequip_item(obj=item)
        self.inventory.remove(item)

    def equip_item(self, name=None, obj=None):
        """Equips an item in the player's inventory"""

        item = self._find_by_name_or_obj(name, obj)
        if item.category not in self.equippable_types:
            raise ItemNotEquippableError(
                f"{item.name} is of type {item.category} which is not an "
                f"equippable type {', '.join(self.equippable_types)}"
            )
        if item.category == 'weapon':
            item.equipped = True
            if self.equipped_weapon is not None:
                self.unequip_item(obj=self.equipped_weapon)
            self.equipped_weapon = item
            self.console.chat(f"{self.name} takes up {item.name} as their weapon of choice.")
        elif item.category == 'armor':
            item.equipped = True
            if self.equipped_armor is not None:
                self.unequip_item(obj=self.equipped_armor)
            self.equipped_armor = item
            self.console.chat(f"{self.name} dons {item.name} as their armor of choice.")
        else:
            raise Exception(f'Somehow an equippable item type was not equippable: {item.name}')
        return None

    def unequip_item(self, name=None, obj=None):
        """Unequips an item in the player's inventory"""

        item = self._find_by_name_or_obj(name, obj)
        if not item.equipped:
            raise ItemNotEquippedError(f"{item.equipped} is not currently set to equipped.")
        elif item.category == 'weapon':
            self.equipped_weapon = None
        elif item.category == 'armor':
            self.equipped_armor = None
        item.equipped = False
        self.console.chat(f"{self.name} unequips {item.name}.")
        return None

    def find_inventory_item_by_name(self, name):
        """Retrieves a inventory item object using all or part of the name"""

        name = name.lower()
        matching_items = [
            itm for itm in self.inventory if name in itm.name.lower()
        ]
        if len(matching_items) == 0:
            raise ItemNotFoundError(f"{name} not found in {[i.name for i in self.inventory]}")
        item = matching_items[0]  # Best effort guess at match
        return item

    def _find_by_name_or_obj(self, name, obj):
        """Retrieves an Item object by name, or simply returns the given object

        This logic handles situations when we already have the object we want, but more importantly
        (as this game uses chat commands) when we only have all or part of the item name.
        """

        if (name is None and obj is None) or (name is not None and obj is not None):
            raise ValueError(
                f"Must pass either a name or an object! name={name}, obj={obj} is invalid."
            )
        elif name is not None:
            item = self.find_inventory_item_by_name(name)
        elif obj is not None:
            item = obj
        return item

    def show_inventory(self):
        """Displays the contents of the player's inventory in (hopefully) readable fashion.

        Format is as follows: name (strength) (category)
        Example: `sword (10) (w)`  -- A sword with a strength of 10 and categorized as a weapon (w).
        """

        entries = []
        for itm in self.inventory:
            entries.append(f"{'*' if itm.equipped else ''} {itm.name} ({itm.strength}) ({itm.category[0]})")
        inv = ', '.join(entries)
        return inv

    @property
    def defense(self):
        """Player's defense score as calculated on-the-fly to avoid stale stats.

        Currently a player's defense is calculated by taking the sum of equipped armor's strength
        (or 0 is nothing is equipped) and the player's agility.
        """

        if not self.equipped_armor:
            armor_str = 0
        else:
            armor_str = self.equipped_armor.strength
        dfns = armor_str + self.agility
        return dfns

    @property
    def damage(self):
        """Player's damage score as calculated on-the-fly to avoid stale stats.

        Currently damage is calculated by taking the sum of any equipped weapon's strength
        (or 0 if nothing is equipped) and the player's strength.
        """

        if not self.equipped_weapon:
            weap_str = 0
        else:
            weap_str = self.equipped_weapon.strength
        dmg = weap_str + self.strength
        return dmg
