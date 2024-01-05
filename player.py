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


class Player:
    def __init__(self, piece: Piece, name: str):
        self.name = name
        self.balance = 1500
        self.piece = piece
        self.location = None
        self.properties = []
        self.debt = 0
        self.debt_to = None
        self.in_jail = False
        self.jail_turns_left = 0
        self.last_roll = None
        self.property_manager = None

    def calculate_net_worth(self):
        return self.balance + sum([prop.get_value() for prop in self.properties])

    def land(self):
        self.location.space.effect(self)

    def __any_un_mortgaged_properties(self):
        for prop in self.properties:
            if not prop.mortgaged:
                return True
        return False

    def charge(self, amount: int, recipient):
        if amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
        elif self.__any_un_mortgaged_properties():
            amount_paid = self.balance
            recipient.balance += amount_paid
            self.balance = 0
            self.debt = amount - amount_paid
            self.debt_to = recipient
        else:
            pass  # you lose

    def pay_debt(self):
        if self.debt_to is None:
            raise Exception("Can't pay debt when not in debt")
        if self.balance < self.debt:
            raise Exception("Not enough to pay debt")
        self.balance -= self.debt
        self.debt_to.balance += self.debt
        self.debt = 0
        self.debt_to = None

    def go_to_jail(self):
        while not isinstance(self.location.space, Jail):
            self.location = self.location.next
        self.in_jail = True
        self.jail_turns_left = 2

    def purchase_location(self):
        if self.location.space is not Property:
            raise Exception("Can't purchase a space that isn't property")
        if self.location.space.owner is not None:
            raise Exception("Can't purchase already owned property")
        if self.balance < self.location.space.price:
            raise Exception("Not enough balance to buy property")

        self.balance -= self.location.space.price
        self.property_manager.claim(self.location.space, self)

    def __search_for_property(self, property_name: str):
        for prop in self.properties:
            if prop.name == property_name:
                return prop
        raise Exception("No property by that name")

    def mortgage(self, property_name: str):
        self.__search_for_property(property_name).mortgage()

    def un_mortgage(self, property_name: str):
        self.__search_for_property(property_name).un_mortgage()

