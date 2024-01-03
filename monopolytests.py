import unittest
from monopolygame import MonopolyGame
from player import Player, Piece
from go import Go

p1 = Player(Piece.SHOE, "Dan")
p2 = Player(Piece.BATTLESHIP, "Chris")
p3 = Player(Piece.THIMBLE, "Lucas")

monopoly = MonopolyGame([p1, p2, p3])


class MonopolyTestCases(unittest.TestCase):
    def test_starting_locations(self):
        self.assertTrue(isinstance(p1.location.space, Go))
        self.assertTrue(isinstance(p2.location.space, Go))
        self.assertTrue(isinstance(p3.location.space, Go))

    def test_starting_inventories(self):
        self.assertEqual(1500, p1.balance)
        self.assertEqual(1500, p2.balance)
        self.assertEqual(1500, p3.balance)
        self.assertListEqual(p1.properties, [])
        self.assertListEqual(p2.properties, [])
        self.assertListEqual(p3.properties, [])


if __name__ == '__main__':
    unittest.main()
