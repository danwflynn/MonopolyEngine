from space import Space


class Tax(Space):
    def __init__(self, name: str, game):
        super().__init__(name)
        self.game = game


class IncomeTax(Tax):
    def __init__(self, game):
        super().__init__("Income Tax", game)

    def effect(self, player):
        amount = min(200, int(0.1 * player.calculate_net_worth()))
        player.charge(amount, self.game.free_parking_node.space)


class LuxuryTax(Tax):
    def __init__(self, game):
        super().__init__("Luxury Tax", game)

    def effect(self, player):
        player.charge(75, self.game.free_parking_node.space)
