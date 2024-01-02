from enum import Enum
from properties import Property


class Piece(Enum):
    TOP_HAT = "Top Hat"
    SHOE = "Shoe"
    DOG = "Dog"
    BATTLESHIP = "Battleship"
    THIMBLE = "Thimble"
    WHEELBARROW = "Wheelbarrow"
    CAT = "Cat"
    RACECAR = "Racecar"


class Player:
    def __init__(self, piece: Piece, name: str):
        self.name = name
        self.balance = 1500
        self.piece = piece
        self.location = None
        self.properties = [Property]
        self.debt = 0
        self.jailTurns = 0
