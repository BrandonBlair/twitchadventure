from random import choice as pick


class NameGenerator(object):
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = [
        'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w',
        'x', 'y', 'z'
    ]
    openers = ['dr', 'th', 'ph', 'sh', 'br', 'pl', 'sr', 'am', 'an', 'en', 'ed', 'tr', 'tl']
    closers = ['rs', 'rz', 'nd', 'rd', 'rb', 'rn', 'th', 'sh', 'ph']
    # Use sets to avoid dupes but retain lists because sets aren't indexable for random.choice
    flavors = list(
        set(openers).union(
            set(closers).union(
                set(['dl', 'zr', 'rn', 'nr', 'dn'])
            )
        )
    )

    @property
    def styles(self):
        styls = {
            'simple': (
                f"{pick(self.vowels)}"
                f"{pick(self.flavors)}"
                f"{pick(self.vowels)}"
            ),
            'medium': (
                f"{pick(self.openers)}"
                f"{pick(self.vowels)}"
                f"{pick(self.closers)}"
            ),
            'long': (
                f"{pick(self.vowels)}"
                f"{pick(self.flavors)}"
                f"{pick(self.vowels)}"
                f"{pick(self.consonants)}"
            ),
            'longer': (
                f"{pick(self.vowels)}"
                f"{pick(self.flavors)}"
                f"{pick(self.vowels)}"
                f"{pick(self.consonants)}"
                f"{pick(self.vowels)}"
                f"{pick(self.closers)}"
            ),
        }
        return styls


def random_name():
    generator = NameGenerator()
    pool = list(generator.styles.values())
    randomly_chosen = pick(pool)
    return randomly_chosen
