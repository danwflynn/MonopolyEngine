from model.space import Space


class FreeParking(Space):
    def __init__(self):
        super().__init__("Free Parking")
        self.balance = 0

    def effect(self, player):
        player.balance += self.balance
        self.balance = 0
