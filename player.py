import gamemap

class PlayerEventHandlers(object):
    def __init__(self):
        pass

class Player(object):
    """A human player"""

    def __init__(self, name, map):
        self.name = name
        self.map = map
        self.handlers = None

    def begin_turn(self):
        """Perform a turn's actions"""
        pass


