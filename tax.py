from space import Space


class Tax(Space):
    def __init__(self, name: str, game):
        super().__init__(name)
        self.game = game


class IncomeTax(Tax):
    def __init__(self, game):
        super().__init__("Income Tax", game)

    def effect(self, player):
        amount = min(200, 0.1 * player.calculate_total_assets())
        player.charge(amount)
        self.game.add_to_jackpot(amount)


class LuxuryTax(Tax):
    def __init__(self, game):
        super().__init__("Luxury Tax", game)

    def effect(self, player):
        player.charge(75)
        self.game.add_to_jackpot(75)
