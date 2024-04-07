from space import Space
from collections import deque
from enum import Enum


class CardType(Enum):
    CHANCE = "Chance"
    COMMUNITY_CHEST = "Community Chest"


class Deed(Space):
    game = None

    def __init__(self, name: str):
        super().__init__(name)


class Card:
    def __init__(self, message: str, f):
        self.message = message
        self.f = f


class GetOutOfJailFreeCard(Card):
    def __init__(self, card_type: CardType):
        super().__init__("Get out of jail free.", lambda player: player.add_jail_free_card())
        self.card_type = card_type


class Chance(Deed):
    cards = deque()
    cards.append(Card("Advance to Boardwalk.", lambda player: player.advance_to("Boardwalk")))
    cards.append(Card("Advance to St. Charles Place. If you pass \"Go\" collect $200.",
                      lambda player: player.advance_to("St. Charles Place")))
    cards.append(GetOutOfJailFreeCard(CardType.CHANCE))
    cards.append(Card("Take a trip to Reading Railroad. If you pass \"Go\" collect $200.",
                      lambda player: player.advance_to("Reading Railroad")))
    cards.append(Card("Go back three spaces.", lambda player: player.go_back(3)))
    cards.append(Card("Advance to the nearest railroad. If unowned, you may buy it from the bank. "
                      "If owned, pay the owner twice the rental to which they are otherwise entitled.",
                      lambda player: player.go_nearest_railroad()))
    cards.append(Card("Bank pays you dividend of $50.", lambda player: player.collect(50)))
    cards.append(Card("Go to jail. Go directly to jail, do not pass \"Go\", do not collect $200.",
                      lambda player: player.go_to_jail()))
    cards.append(Card("Your building loan matures. Collect $150.", lambda player: player.collect(150)))
    cards.append(Card("Advance to \"Go\". (Collect $200)", lambda player: player.advance_to("Go")))
    cards.append(Card("Make general repairs on all you property: for each house pay $25, for each hotel pay $100.",
                      lambda player: player.charge(player.repair_costs(25, 100), Deed.game.free_parking_node.space)))
    cards.append(Card("Speeding fine $15.", lambda player: player.charge(15, Deed.game.free_parking_node.space)))
    cards.append(Card("Advance to the nearest utility. If unowned, you may buy it from the bank."
                      "If owned, throw dice and pay owner a total ten times amount thrown.",
                      lambda player: player.go_nearest_utility()))
    cards.append(Card("Advance to Illinois Avenue. If you pass \"Go\" collect $200.",
                      lambda player: player.advance_to("Illinois Avenue")))
    cards.append(Card("You have been elected chairman of the board. Pay each player $50",
                      lambda player: player.pay_each(50, [x for x in Deed.game.players if x is not player])))
    cards.append(Card("Advance to the nearest railroad. If unowned, you may buy it from the bank."
                      "If owned, pay the owner twice the rental to which they are otherwise entitled.",
                      lambda player: player.go_nearest_railroad()))

    def __init__(self):
        super().__init__("Chance")

    def effect(self, player):
        is_get_out_of_jail_free = isinstance(self.cards[0], GetOutOfJailFreeCard)
        self.cards[0].f(player)
        if not is_get_out_of_jail_free:
            self.cards.rotate(-1)


class CommunityChest(Deed):
    cards = deque()

    cards.append(Card("Advance to \"Go\". (Collect $200)", lambda player: player.advance_to("Go")))
    cards.append(Card("Bank error in your favor. Collect $200.", lambda player: player.collect(200)))
    cards.append(Card("Doctor's fees. Pay $50", lambda player: player.charge(50, Deed.game.free_parking_node.space)))
    cards.append(GetOutOfJailFreeCard(CardType.COMMUNITY_CHEST))
    cards.append(Card("Go directly to jail. Do not pass Go, Do not collect $200.", lambda player: player.go_to_jail()))
    cards.append(Card("Grand Opera Night. Collect $50 from every player for opening night seats.",
                      lambda player: player.charge_each(50, [x for x in Deed.game.players if x is not player])))
    cards.append(Card("Holiday Fund matures. Receive $100.", lambda player: player.collect(100)))
    cards.append(Card("Income tax refund. Collect $20.", lambda player: player.collect(20)))
    cards.append(Card("It is your birthday. Collect $10 from every player.",
                      lambda player: player.charge_each(10, [x for x in Deed.game.players if x is not player])))
    cards.append(Card("Life insurance matures. Collect $100", lambda player: player.collect(100)))
    cards.append(Card("Hospital Fees. Pay $50.", lambda player: player.charge(50, Deed.game.free_parking_node.space)))
    cards.append(Card("School Fees. Pay $50.", lambda player: player.charge(50, Deed.game.free_parking_node.space)))
    cards.append(Card("Receive $25 consultancy fee", lambda player: player.collect(25)))
    cards.append(Card("You are assessed for street repairs: Pay $40 per house and $115 per hotel you own.",
                      lambda player: player.charge(player.repair_costs(40, 115), Deed.game.free_parking_node.space)))
    cards.append(Card("You have won second prize in a beauty contest. Collect $10.", lambda player: player.collect(10)))
    cards.append(Card("You inherit $100.", lambda player: player.collect(100)))

    def __init__(self):
        super().__init__("Community Chest")

    def effect(self, player):
        is_get_out_of_jail_free = isinstance(self.cards[0], GetOutOfJailFreeCard)
        self.cards[0].f(player)
        if not is_get_out_of_jail_free:
            self.cards.rotate(-1)
