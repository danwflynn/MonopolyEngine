from space import Space
from collections import deque


class Deed(Space):
    def __init__(self, name: str, game):
        super().__init__(name)
        self.cards = deque()
        self.game = game


class Card:
    def __init__(self, message: str, f):
        self.message = message
        self.f = f


class Chance(Deed):
    def __init__(self, game):
        super().__init__("Chance", game)
        self.cards.append(Card("Advance to Boardwalk.", lambda player: player.advance_to("Boardwalk")))
        self.cards.append(Card("Advance to St. Charles Place. If you pass \"Go\" collect $200.",
                               lambda player: player.advance_to("St. Charles Place")))
        self.cards.append(Card("Get out of jail free.", lambda player: player.add_jail_free_card()))
        self.cards.append(Card("Take a trip to Reading Railroad. If you pass \"Go\" collect $200.",
                               lambda player: player.advance_to("Reading Railroad")))
        self.cards.append(Card("Go back three spaces.", lambda player: player.go_back(3)))
        self.cards.append(Card("Advance to the nearest railroad. If unowned, you may buy it from the bank."
                               "If owned, pay the owner twice the rental to which they are otherwise entitled.",
                               lambda player: player.go_nearest_railroad()))
        self.cards.append(Card("Bank pays you dividend of $50.", lambda player: player.collect(50)))
        self.cards.append(Card("Go to jail. Go directly to jail, do not pass \"Go\", do not collect $200.",
                               lambda player: player.go_to_jail()))
        self.cards.append(Card("Your building loan matures. Collect $150.", lambda player: player.collect(150)))
        self.cards.append(Card("Advance to \"Go\". (Collect $200)", lambda player: player.advance_to_go()))
        self.cards.append(Card("Make general repairs on all you property: for each house pay $25, for each hotel"
                               "pay $100.", lambda player: player.charge(player.repair_costs(25, 100),
                                                                         self.game.free_parking_node.space)))
        self.cards.append(Card("Speeding fine $15.", lambda player: player.charge(15,
                                                                                  self.game.free_parking_node.space)))
        self.cards.append(Card("Advance to the nearest utility. If unowned, you may buy it from the bank."
                               "If owned, throw dice and pay owner a total ten times amount thrown.",
                               lambda player: player.go_nearest_utility()))
        self.cards.append(Card("Advance to Illinois Avenue. If you pass \"Go\" collect $200.",
                               lambda player: player.advance_to("Illinois Avenue")))
        self.cards.append(Card("You have been elected chairman of the board. Pay each player $50",
                               lambda player: player.pay_each(50, [x for x in self.game.players if x is not player])))
        self.cards.append(Card("Advance to the nearest railroad. If unowned, you may buy it from the bank."
                               "If owned, pay the owner twice the rental to which they are otherwise entitled.",
                               lambda player: player.go_nearest_railroad()))


class CommunityChest(Deed):
    def __init__(self, game):
        super().__init__("Community Chest", game)
