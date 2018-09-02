from game.escape.escape_room import EscapeRoom, Step


class CabinMystery(EscapeRoom):

    name = "The Mysterious Cabin"

    def __init__(self):
        super().__init__()
        self.steps = [
            CarInterior(),
            CarExterior(),
        ]
        self.inventory = []


class CarInterior(Step):
    solution_set = {'unlock', 'door'}
    success_msg = "You "
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