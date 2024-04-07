from model.space import Space


class GoToJail(Space):
    def __init__(self):
        super().__init__("Go to Jail")

    def effect(self, player):
        player.go_to_jail()


class Jail(Space):
    def __init__(self):
        super().__init__("Jail")
