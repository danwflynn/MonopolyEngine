from monopolygame import MonopolyGame
from player import *

p1 = Player(Piece.SHOE, "Dan")
p2 = Player(Piece.BATTLESHIP, "Chris")
p3 = Player(Piece.THIMBLE, "Lucas")

monopoly = MonopolyGame([p1, p2, p3])

p = Property("a", 1, 2, 3)
print(p.name)
