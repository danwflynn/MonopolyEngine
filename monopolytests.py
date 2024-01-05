import unittest
from monopolygame import MonopolyGame
from player import Player, Piece
from go import Go
from jail import Jail
from freeparking import FreeParking


class MonopolyTestCases(unittest.TestCase):
    def setUp(self):
        self.p1 = Player(Piece.SHOE, "Dan")
        self.p2 = Player(Piece.BATTLESHIP, "Chris")
        self.p3 = Player(Piece.THIMBLE, "Lucas")
        self.monopoly = MonopolyGame([self.p1, self.p2, self.p3])

    def test_starting_locations(self):
        self.assertTrue(isinstance(self.p1.location.space, Go))
        self.assertTrue(isinstance(self.p2.location.space, Go))
        self.assertTrue(isinstance(self.p3.location.space, Go))

    def test_starting_inventories(self):
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(1500, self.p2.balance)
        self.assertEqual(1500, self.p3.balance)
        self.assertListEqual(self.p1.properties, [])
        self.assertListEqual(self.p2.properties, [])
        self.assertListEqual(self.p3.properties, [])

    def test_roll_no_doubles(self):
        self.monopoly.roll(6, 4)
        self.assertFalse(self.monopoly.roll_available)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.players[0], self.p2)
        self.assertEqual(self.monopoly.players[1], self.p3)
        self.assertEqual(self.monopoly.players[2], self.p1)
        self.assertTrue(self.monopoly.roll_available)

    def test_roll_doubles(self):
        self.monopoly.roll(5, 5)
        self.assertFalse(self.monopoly.roll_available)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.assertEqual(1, self.monopoly.doubles_in_a_row)
        self.monopoly.roll(5, 3)
        self.assertEqual(0, self.monopoly.doubles_in_a_row)
        self.assertEqual("Tennessee Avenue", self.p1.location.space.name)
        self.monopoly.end_turn()

    def test_roll_three_doubles(self):
        self.monopoly.roll(5, 5)
        self.assertFalse(self.monopoly.roll_available)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.assertEqual(1, self.monopoly.doubles_in_a_row)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.monopoly.roll(5, 5)
        self.assertTrue(isinstance(self.p1.location.space, FreeParking))
        self.assertEqual(2, self.monopoly.doubles_in_a_row)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, Jail))

    def test_land_on_go_to_jail(self):
        self.monopoly.roll(5, 5)
        self.assertFalse(self.monopoly.roll_available)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.assertEqual(1, self.monopoly.doubles_in_a_row)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.players[0], self.p1)
        self.assertEqual(self.monopoly.players[1], self.p2)
        self.assertEqual(self.monopoly.players[2], self.p3)
        self.monopoly.roll(5, 5)
        self.assertTrue(isinstance(self.p1.location.space, FreeParking))
        self.assertEqual(2, self.monopoly.doubles_in_a_row)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, Jail))

    def test_escape_jail1(self):
        self.p1.go_to_jail()
        self.monopoly.jail_roll(5, 5)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, FreeParking))
        self.assertEqual(self.monopoly.players[0], self.p2)
        self.assertEqual(self.monopoly.players[1], self.p3)
        self.assertEqual(self.monopoly.players[2], self.p1)


if __name__ == '__main__':
    unittest.main()
