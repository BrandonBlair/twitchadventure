from game.adventure.asset import Asset


class Character(Asset):

    def __init__(self, name, race, strength=1, max_health=100, gold=0, perception=1):
        self.name = name
        self.race = race

        self.strength = strength
        self.max_health = max_health
        self.health = self.max_health
        self.perception = perception

        self.inventory = []
        self.gold = gold

    def add_gold(self, amount):
        self.gold += amount

    def remove_gold(self, amount):
        self.gold -= amount

    def give_item(self, item):
        self.inventory.append(item)

    def take_item(self, item):
        self.inventory.remove(item)

