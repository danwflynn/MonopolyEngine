from space import Space
from enum import Enum


class Color(Enum):
    BROWN = "Brown"
    LIGHT_BLUE = "Light Blue"
    MAGENTA = "Magenta"
    ORANGE = "Orange"
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    DARK_BLUE = "Dark Blue"


class Property(Space):
    def __init__(self, name: str, price: int, rent, mortgage: int):
        super().__init__(name)
        self.price = price
        self.owner = None
        self.rent = rent
        self.mortgage = mortgage
        self.mortgaged = False

    def effect(self, player):
        if self.owner is not None and self.owner is not player:
            player.charge(self.rent)
            self.owner.balance += self.rent


class Housing(Property):
    def __init__(self, name: str, price: int, mortgage: int, color: Color, building_cost: int,
                 rents: (int, int, int, int, int, int)):
        super().__init__(name, price, rents[0], mortgage)
        self.color = color
        self.monopolized = False
        self.houses = 0
        self.hotels = 0
        self.building_cost = building_cost
        self.rents = rents


class Railroad(Property):
    def __init__(self, name: str):
        super().__init__(name, 200, 25, 100)


class Utility(Property):
    def __init__(self, name: str):
        super().__init__(name, 150, None, 75)
        self.both_owned = False

    def effect(self, player):
        factor = 10 if self.both_owned else 4
        if self.owner is not None and self.owner is not player:
            player.charge(factor * player.last_roll)
            self.owner.balance += self.rent


class ElectricCompany(Utility):
    def __init__(self):
        super().__init__("Electric Company")


class WaterWorks(Utility):
    def __init__(self):
        super().__init__("Water Works")
