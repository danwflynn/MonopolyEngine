from space import Space
from collections import deque


class Deed(Space):
    def __init__(self, name: str, game):
        super().__init__(name)
        self.cards = deque()
        self.game = game


class Card:
    def __init__(self, message: str, f):
        self.message = message
        self.f = f


class Chance(Deed):
    def __init__(self, game):
        super().__init__("Chance", game)
        self.cards.append(Card("Advance to boardwalk", lambda x: x))


class CommunityChest(Deed):
    def __init__(self, game):
        super().__init__("Community Chest", game)
