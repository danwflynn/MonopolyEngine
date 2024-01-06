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
        self.bankrupt = False
        self.jail_free_cards = 0

    def calculate_net_worth(self):
        return self.balance + sum([prop.get_value() for prop in self.properties])

    def land(self):
        self.location.space.effect(self)

    def __any_un_mortgaged_properties(self):
        for prop in self.properties:
            if not prop.mortgaged:
                return True
        return False

    def collect(self, amount: int):
        self.balance += amount

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
            recipient.balance += self.balance
            self.balance = 0
            for prop in self.properties:
                self.property_manager.reset(prop)
                self.properties.remove(prop)
                self.bankrupt = True

    def liquidate_everything(self):
        for prop in [x for x in self.properties if isinstance(x, Housing)]:
            if prop.hotels:
                self.property_manager.sell_hotel(prop)
            self.property_manager.sell_houses(prop, prop.houses)
        for prop in [x for x in self.properties if not x.mortgaged]:
            prop.mortgage()

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
        if not isinstance(self.location.space, Property):
            raise Exception(f'Can\'t purchase {self.location.space.name} because it isn\'t property')
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

    def player_mortgage(self, property_name: str):
        self.__search_for_property(property_name).prop_mortgage()

    def player_un_mortgage(self, property_name: str):
        self.__search_for_property(property_name).prop_un_mortgage()

    def build_houses(self, property_name: str, n: int):
        self.property_manager.build_houses(self.__search_for_property(property_name), n)

    def build_hotel(self, property_name: str):
        self.property_manager.build_hotel(self.__search_for_property(property_name))

    def sell_houses(self, property_name: str, n: int):
        self.property_manager.sell_houses(self.__search_for_property(property_name), n)

    def sell_hotel(self, property_name: str):
        self.property_manager.sell_hotel(self.__search_for_property(property_name))
