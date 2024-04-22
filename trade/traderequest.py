from typing import List


class TradeRequest:
    def __init__(self, players):
        self.players = players
        self.gives = {}
        self.receives = {}
        for player in players:
            self.gives[player] = ([], 0, None)
            self.receives[player] = ([], 0, None)
