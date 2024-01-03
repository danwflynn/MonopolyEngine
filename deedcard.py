from space import Space
from collections import deque


class DeedCard(Space):
    def __init__(self, name: str, game):
        super().__init__(name)
        self.cards = deque()
        self.game = game


class Chance(DeedCard):
    def __init__(self, game):
        super().__init__("Chance", game)


class CommunityChest(DeedCard):
    def __init__(self, game):
        super().__init__("Community Chest", game)
