from space import Space
from collections import deque


class DeedCard(Space):
    def __init__(self, name: str):
        super().__init__(name)
        self.cards = deque()


class Chance(DeedCard):
    def __init__(self):
        super().__init__("Chance")


class CommunityChest(DeedCard):
    def __init__(self):
        super().__init__("Community Chest")
