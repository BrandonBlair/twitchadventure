class PlayerExistsInCampaignError(ValueError):
    pass

class CharacterExistsInRoomError(ValueError):
    pass

class CharacterNotInRoomError(ValueError):
    pass

class ItemNotFoundError(ValueError):
    pass

class ItemNotEquippableError(ValueError):
    pass

class ItemNotEquippedError(ValueError):
    pass

class InvalidTargetError(ValueError):
    pass
