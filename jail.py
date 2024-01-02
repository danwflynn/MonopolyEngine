from space import Space


class GoToJail(Space):
    def __init__(self):
        super().__init__("Go to Jail")


class Jail(Space):
    def __init__(self):
        super().__init__("Jail")
