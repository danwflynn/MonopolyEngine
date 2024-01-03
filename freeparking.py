from space import Space


class FreeParking(Space):
    def __init__(self):
        super().__init__("Free Parking")
        self.jackpot = 0

    def effect(self, player):
        player.balance += self.jackpot
        self.jackpot = 0
