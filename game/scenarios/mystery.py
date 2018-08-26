from game.adventure_game import AdventureGame, Step


class CabinMystery(AdventureGame):

    name = "The Mysterious Cabin"

    def __init__(self):
        super().__init__()
        self.steps = [
            CarInterior(),
            CarExterior(),
        ]


class CarInterior(Step):
    solution_set = {'unlock', 'door'}
    success_msg = "Nice job, figuring out you need to unlock a door to walk through it."
    desc = (
        "You wake up in the driver seat of a car. "
        "It is raining steadily and very dark outside. "
        "The engine is running."
    )

class CarExterior(Step):
    solution_set = {'check', 'pockets'}
    success_msg = "I think you're getting the hang of this!"
    desc = (
        "You are standing outside a 1991 Ford Taurus. "
        "The hazards are blinking and rain is pattering "
        "on your hair and clothes. You can't see anything "
        "beyond the area surrounding the car."
    )