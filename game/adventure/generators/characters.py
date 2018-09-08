from random import choice, randrange
from game.adventure.generators.names import random_name
from game.adventure.races import races
from game.adventure.character import Character
from game.adventure.generators.loot import random_loot


def random_character(console):
    mystery_char = Character(
        console=console,
        name=random_name(),
        race=choice(races),
        strength=randrange(1, 7),
        max_health=randrange(10, 101),
        gold=randrange(0, 30),
        perception=randrange(1,16),
        agility=randrange(1,8)
    )

    mystery_char.inventory = [
        random_loot()
    ]

    return mystery_char
