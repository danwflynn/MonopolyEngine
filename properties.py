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
            player.charge(self.rent, self.owner)

    def get_value(self):
        if not self.mortgaged:
            return self.price
        else:
            return self.price / 2

    def mortgage(self):
        if self.owner is None:
            raise Exception("Can't mortgage an unowned property")
        if self.mortgaged:
            raise Exception("Can't mortgage already mortgaged property")
        self.mortgaged = True
        self.owner.balance += self.mortgage

    def un_mortgage(self):
        if self.owner is None:
            raise Exception("Can't un-mortgage an unowned property")
        if not self.mortgaged:
            raise Exception("Can't un-mortgage already un-mortgaged property")
        if self.owner.balance < int(1.1 * self.mortgage):
            raise Exception("Can't afford to un-mortgage")
        self.mortgaged = False
        self.owner.balance -= int(1.1 * self.mortgage)

    def reset(self):
        self.owner = None
        self.mortgaged = False


class Housing(Property):
    def __init__(self, name: str, price: int, mortgage: int, color: Color, building_cost: int,
                 rents: (int, int, int, int, int, int)):
        super().__init__(name, price, rents[0], mortgage)
        self.color = color
        self.houses = 0
        self.hotels = 0
        self.building_cost = building_cost
        self.rents = rents

    def get_value(self):
        return super().get_value() + (self.houses * self.building_cost) + (5 * self.hotels * self.building_cost)

    def mortgage(self):
        if self.houses + self.hotels != 0:
            raise Exception(f'Can\'t mortgage {self.name} with buildings on it')
        Property.mortgage(self)

    def reset(self):
        if self.houses + self.hotels > 0:
            raise Exception(f'Can\'t reset {self.name} when there are buildings present')
        super().reset()
        self.rent = self.rents[0]


class Railroad(Property):
    def __init__(self, name: str):
        super().__init__(name, 200, 25, 100)

    def reset(self):
        super().reset()
        self.rent = 25


class Utility(Property):
    def __init__(self, name: str):
        super().__init__(name, 150, None, 75)
        self.both_owned = False

    def effect(self, player):
        factor = 10 if self.both_owned else 4
        if self.owner is not None and self.owner is not player:
            player.charge(factor * player.last_roll, self.owner)

    def reset(self):
        super().reset()
        self.both_owned = False


class ElectricCompany(Utility):
    def __init__(self):
        super().__init__("Electric Company")


class WaterWorks(Utility):
    def __init__(self):
        super().__init__("Water Works")
