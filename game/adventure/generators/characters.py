from random import choice, randrange, uniform
from game.adventure.generators.names import random_name
from game.adventure.races import races
from game.adventure.character import Character
from game.adventure.generators.loot import random_loot


def random_character(console, avg_player_level):
    difficulty_modifier = uniform(.50, 1.50)

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
