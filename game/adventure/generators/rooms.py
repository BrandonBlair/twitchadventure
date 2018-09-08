from random import choice as pick

from game.adventure.room import Room
from game.adventure.generators.characters import random_character
from game.adventure.chat_tools import title_case


class RoomGenerator(object):
    areas = [
        'staircase',
        'room',
        'hallway',
        'chamber',
        'scullery',
        'parlor',
        'conservatory',
        'study',
        'drawing room',
        'dining area',
    ]

    adverbs = [
        'moderately',
        'surprisingly',
        'curiously',
        'subtly',
        'deceivingly'
    ]

    adjectives = [
        'large',
        'well-lit',
        'expansive',
        'cloistered',
        'small',
        'spacious',
        'shadowy',
        'tucked-away',
    ]

    atmospherics = [
        'An oil lamp flickers on the wall.',
        'You hear the steady patter of water dripping.',
        'An ominous silence strangles this place.',
        'This place almost feels forgotten.',
        'The site of this place sturs some distant memory... ',
    ]

    def gen_desc(self, area):
        desc = (
            f"You are in a {pick(self.adverbs)} {pick(self.adjectives)} "
            f"{area}. {pick(self.atmospherics)}"
        )
        return desc

    def gen_name(self, area):
        name = f"The {title_case(area)}"
        return name

def random_room(console):
    generator = RoomGenerator()
    random_area = pick(generator.areas)
    mystery_room = Room(
        console=console,
        name=generator.gen_name(random_area),
        desc=generator.gen_desc(random_area)
    )
    mystery_room.add_character(
        character=random_character(console)
    )
    return mystery_room