from gamemodel.properties import *
from gamemodel.jail import Jail
from gamemodel.go import Go
from gamemodel.deed import *


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
        self.jail_free_cards = []
        self.rent_multiplier = 1

    def calculate_net_worth(self):
        return self.balance + sum([prop.get_value() for prop in self.properties])

    def land(self):
        self.location.space.effect(self)
        self.rent_multiplier = 1

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
        else:
            amount_paid = self.balance
            recipient.balance += amount_paid
            self.balance = 0
            self.debt += amount - amount_paid
            self.debt_to = recipient

    def liquidate_everything(self):
        for prop in [x for x in self.properties if isinstance(x, Housing)]:
            if prop.hotels:
                self.property_manager.sell_hotel(prop)
        for i in range(4):
            for prop in [x for x in self.properties if isinstance(x, Housing)]:
                if prop.houses:
                    self.property_manager.sell_houses(prop, 1)
        for prop in [x for x in self.properties if not x.mortgaged]:
            prop.prop_mortgage()

    def pay_debt(self):
        if self.debt_to is None:
            raise Exception("Can't pay debt when not in debt")
        if self.balance < self.debt:
            raise Exception("Not enough to pay debt")
        self.balance -= self.debt
        if isinstance(self.debt_to, Player):
            self.debt_to.balance += self.debt
        else:
            amount_per_player = self.debt / len(self.debt_to)
            for player in self.debt_to:
                player.balance += amount_per_player
        self.debt = 0
        self.debt_to = None

    def declare_bankruptcy(self):
        if self.debt <= self.balance or self.__any_un_mortgaged_properties():
            raise Exception("Cannot declare bankruptcy")
        if isinstance(self.debt_to, Player):
            self.debt_to.balance += self.balance
        else:
            amount_per_player = self.balance / len(self.debt_to)
            for player in self.debt_to:
                player.balance += amount_per_player
        for prop in self.properties:
            self.property_manager.reset(prop)
        self.properties.clear()
        self.bankrupt = True
        self.balance = 0

    def go_to_jail(self):
        while not isinstance(self.location.space, Jail):
            self.location = self.location.next
        self.in_jail = True
        self.jail_turns_left = 2

    def advance_to(self, property_name: str):
        while self.location.space.name != property_name:
            self.location = self.location.next
            if isinstance(self.location.space, Go):
                self.balance += 200
        self.land()

    def add_jail_free_card(self, card: GetOutOfJailFreeCard):
        self.jail_free_cards.append(card)
        if card.card_type is CardType.CHANCE:
            Chance.cards.remove(card)
        else:
            CommunityChest.cards.remove(card)

    def use_jail_free_card(self):
        if self.jail_free_cards[0].card_type is CardType.CHANCE:
            Chance.cards.append(self.jail_free_cards[0])
        else:
            CommunityChest.cards.append(self.jail_free_cards[0])
        self.jail_free_cards.pop(0)

    def go_back(self, n: int):
        for i in range(n):
            self.location = self.location.prev
        self.land()

    def go_nearest_railroad(self):
        while not isinstance(self.location.space, Railroad):
            self.location = self.location.next
            if isinstance(self.location.space, Go):
                self.balance += 200
        self.rent_multiplier = 2
        self.land()

    def go_nearest_utility(self):
        while not isinstance(self.location.space, Utility):
            self.location = self.location.next
            if isinstance(self.location.space, Go):
                self.balance += 200
        self.rent_multiplier = str
        self.land()

    def repair_costs(self, house_repair_cost: int, hotel_repair_cost: int):
        house_count = 0
        hotel_count = 0
        for prop in self.properties:
            if isinstance(prop, Housing):
                house_count += prop.houses
                hotel_count += prop.hotels
        return (house_count * house_repair_cost) + (hotel_count * hotel_repair_cost)

    def pay_each(self, amount: int, players):
        total_amount = amount * len(players)
        if total_amount <= self.balance:
            self.balance -= total_amount
            for player in players:
                player.balance += amount
        else:
            amount_paid = self.balance
            amount_per_player = self.balance / len(players)
            self.balance = 0
            for player in players:
                player.balance += amount_per_player
            self.debt += total_amount - amount_paid
            self.debt_to = players

    def charge_each(self, amount: int, players):
        for player in players:
            player.charge(amount, self)

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
