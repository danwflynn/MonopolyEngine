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
    def __init__(self, card_type: CardType, message: str, f):
        self.card_type = card_type
        self.message = message
        self.f = f


class GetOutOfJailFreeCard(Card):
    def __init__(self, card_type: CardType):
        super().__init__(card_type, "Get out of jail free.", lambda player: player.add_jail_free_card())


class Chance(Deed):
    cards = deque()
    cards.append(Card(CardType.CHANCE, "Advance to Boardwalk.",
                      lambda player: player.advance_to("Boardwalk")))
    cards.append(Card(CardType.CHANCE, "Advance to St. Charles Place. If you pass \"Go\" collect $200.",
                      lambda player: player.advance_to("St. Charles Place")))
    cards.append(GetOutOfJailFreeCard(CardType.CHANCE))
    cards.append(Card(CardType.CHANCE, "Take a trip to Reading Railroad. If you pass \"Go\" collect $200.",
                      lambda player: player.advance_to("Reading Railroad")))
    cards.append(Card(CardType.CHANCE, "Go back three spaces.", lambda player: player.go_back(3)))
    cards.append(Card(CardType.CHANCE, "Advance to the nearest railroad. If unowned, you may buy it from "
                                       "the bank. "
                                       "If owned, pay the owner twice the rental to which they are "
                                       "otherwise entitled.",
                      lambda player: player.go_nearest_railroad()))
    cards.append(Card(CardType.CHANCE, "Bank pays you dividend of $50.", lambda player: player.collect(50)))
    cards.append(Card(CardType.CHANCE, "Go to jail. Go directly to jail, do not pass \"Go\", do not "
                                       "collect $200.",
                      lambda player: player.go_to_jail()))
    cards.append(Card(CardType.CHANCE, "Your building loan matures. Collect $150.",
                      lambda player: player.collect(150)))
    cards.append(Card(CardType.CHANCE, "Advance to \"Go\". (Collect $200)",
                      lambda player: player.advance_to("Go")))
    cards.append(Card(CardType.CHANCE, "Make general repairs on all you property: for each house pay $25, "
                                       "for each hotel "
                                       "pay $100.",
                      lambda player: player.charge(player.repair_costs(25, 100),
                                                   Deed.game.free_parking_node.space)))
    cards.append(Card(CardType.CHANCE, "Speeding fine $15.",
                      lambda player: player.charge(15,
                                                   Deed.game.free_parking_node.space)))
    cards.append(
        Card(CardType.CHANCE, "Advance to the nearest utility. If unowned, you may buy it from the bank."
                              "If owned, throw dice and pay owner a total ten times amount thrown.",
             lambda player: player.go_nearest_utility()))
    cards.append(Card(CardType.CHANCE, "Advance to Illinois Avenue. If you pass \"Go\" collect $200.",
                      lambda player: player.advance_to("Illinois Avenue")))
    cards.append(Card(CardType.CHANCE, "You have been elected chairman of the board. Pay each player $50",
                      lambda player: player.pay_each(50, [x for x in Deed.game.players if x is not player])))
    cards.append(
        Card(CardType.CHANCE, "Advance to the nearest railroad. If unowned, you may buy it from the bank."
                              "If owned, pay the owner twice the rental to which they are otherwise entitled.",
             lambda player: player.go_nearest_railroad()))

    def __init__(self):
        super().__init__("Chance")


class CommunityChest(Deed):
    cards = deque()

    cards.append(
        Card(CardType.COMMUNITY_CHEST, "Advance to \"Go\". (Collect $200)", lambda player: player.advance_to("Go")))
    cards.append(
        Card(CardType.COMMUNITY_CHEST, "Bank error in your favor. Collect $200.",
             lambda player: player.collect(200)))
    cards.append(Card(CardType.COMMUNITY_CHEST, "Doctor's fees. Pay $50",
                      lambda player: player.charge(50, Deed.game.free_parking_node.space)))
    cards.append(GetOutOfJailFreeCard(CardType.COMMUNITY_CHEST))

    def __init__(self):
        super().__init__("Community Chest")
