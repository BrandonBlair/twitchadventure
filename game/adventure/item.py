class Item(object):
    def __init__(self, name, category='quest', strength=0, required_perception=0):
        self.name = name
        self.category = category
        self.strength = strength
        self.required_perception = required_perception