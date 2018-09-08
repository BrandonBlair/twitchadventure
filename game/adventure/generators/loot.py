from random import choice as pick, randrange

from game.adventure.item import Item


class WeaponGenerator(object):
    nouns = [
        'staff',
        'sword',
        'mace',
        'blackjack',
        'dagger',
        'shiv',
        'rusty chain',
        'chair leg',
    ]

    def gen(self):
        generated_item = Item(
            name=pick(self.nouns),
            category='weapon',
            strength=randrange(1, 7),  # TODO: Scale this to avg level of party and type
            required_perception=randrange(1,10)
        )
        return generated_item

class ArmorGenerator(object):
    nouns = [
        'sackcloth shirt',
        'cloth tunic',
        'leather jerkin',
        'chainmail shirt',
        'silken robe',
        'woven vest',
    ]

    def gen(self):
        generated_item = Item(
            name=pick(self.nouns),
            category='armor',
            strength=randrange(1,7),
            required_perception=randrange(1,10)
        )
        return generated_item

def random_loot():
    generator = pick([WeaponGenerator, ArmorGenerator])
    mystery_item = generator()
    return mystery_item.gen()
