from properties import *
from jail import Jail


class Piece(Enum):
    TOP_HAT = "Top Hat"
    SHOE = "Shoe"
    DOG = "Dog"
    BATTLESHIP = "Battleship"
    THIMBLE = "Thimble"
    WHEELBARROW = "Wheelbarrow"
    CAT = "Cat"
    RACECAR = "Racecar"


monopoly_counts = {
    Color.BROWN: 2,
    Color.LIGHT_BLUE: 3,
    Color.MAGENTA: 3,
    Color.ORANGE: 3,
    Color.RED: 3,
    Color.YELLOW: 3,
    Color.GREEN: 3,
    Color.DARK_BLUE: 2,
}


class Player:
    def __init__(self, piece: Piece, name: str):
        self.name = name
        self.balance = 1500
        self.piece = piece
        self.location = None
        self.properties = []
        self.debt = 0
        self.in_jail = False
        self.jail_turns_left = 0
        self.last_roll = None

    def calculate_total_assets(self):
        return self.balance

    def land(self):
        self.location.space.effect(self)

    def charge(self, amount: int):
        if amount <= self.balance:
            self.balance -= amount
        elif amount <= self.calculate_total_assets():
            pass  # need to sell
        else:
            pass  # you lose

    def go_to_jail(self):
        while self.location.space is not Jail:
            self.location = self.location.next
        self.in_jail = True
        self.jail_turns_left = 3  # might be wrong

    def purchase_location(self):
        if self.location.space is not Property:
            raise Exception("Can't purchase a space that isn't property")
        if self.location.space.owner is not None:
            raise Exception("Can't purchase already owned property")
        if self.balance < self.location.space.price:
            raise Exception("Not enough balance to buy property")

        self.balance -= self.location.space.price
        self.location.space.owner = self
        self.properties.append(self.location.space)

        if isinstance(self.location.space, Housing):
            color = self.location.space.color
            housing_list = [ele for ele in self.properties if isinstance(ele, Housing)]
            housing_group = [prop for prop in housing_list if prop.color == color]
            if len(housing_group) == monopoly_counts[color]:
                for prop in housing_group:
                    prop.monopolized = True
                    prop.rents[0] *= 2
        elif isinstance(self.location.space, Railroad):
            railroad_list = [ele for ele in self.properties if isinstance(ele, Railroad)]
            match len(railroad_list):
                case 2:
                    for railroad in railroad_list:
                        railroad.rent = 50
                case 3:
                    for railroad in railroad_list:
                        railroad.rent = 100
                case 4:
                    for railroad in railroad_list:
                        railroad.rent = 200
        elif isinstance(self.location.space, Utility):
            utility_list = [ele for ele in self.properties if isinstance(ele, Utility)]
            if len(utility_list) == 2:
                for prop in utility_list:
                    prop.both_owned = True

    def mortgage(self, property_name: str):
        if property_name not in [prop.name for prop in self.properties]:
            raise Exception("No property by that name")
        p = None
        for prop in self.properties:
            if prop.name == property_name:
                p = prop
                break
        if p.mortgaged:
            raise Exception("Already mortgaged")
        if isinstance(p, Housing) and (p.houses != 0 or p.hotels != 0):
            raise Exception("Must sell houses before mortgaging")
        p.mortgaged = True
        self.balance += p.mortgage

    def un_mortgage(self, property_name: str):
        if property_name not in [prop.name for prop in self.properties]:
            raise Exception("No property by that name")
        p = None
        for prop in self.properties:
            if prop.name == property_name:
                p = prop
                break
        if not p.mortgaged:
            raise Exception("Already un-mortgaged")
        if int(1.1 * p.mortgage) > self.balance:
            raise Exception("Can't afford to un-mortgage")
        p.mortgaged = True
        self.balance -= int(1.1 * p.mortgage)

