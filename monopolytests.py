import unittest
from monopolygame import MonopolyGame
from player import Player, Piece
from go import Go
from jail import Jail
from freeparking import FreeParking
from properties import *
from tax import *


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
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.active_players[0], self.p2)
        self.assertEqual(self.monopoly.active_players[1], self.p3)
        self.assertEqual(self.monopoly.active_players[2], self.p1)
        self.assertTrue(self.monopoly.roll_available)

    def test_roll_doubles(self):
        self.monopoly.roll(5, 5)
        self.assertFalse(self.monopoly.roll_available)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
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
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
        self.assertEqual(1, self.monopoly.doubles_in_a_row)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
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
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
        self.assertEqual(1, self.monopoly.doubles_in_a_row)
        self.monopoly.end_turn()
        self.assertEqual(self.monopoly.active_players[0], self.p1)
        self.assertEqual(self.monopoly.active_players[1], self.p2)
        self.assertEqual(self.monopoly.active_players[2], self.p3)
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
        self.assertEqual(self.monopoly.active_players[0], self.p2)
        self.assertEqual(self.monopoly.active_players[1], self.p3)
        self.assertEqual(self.monopoly.active_players[2], self.p1)

    def test_bail(self):
        self.p1.go_to_jail()
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(2, self.p1.jail_turns_left)
        self.monopoly.bail()
        self.assertEqual(1450, self.p1.balance)
        self.assertFalse(self.p1.in_jail)
        self.assertEqual(0, self.p1.jail_turns_left)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.monopoly.roll(5, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.assertTrue(isinstance(self.p1.location.space, Housing))

    def test_escape_jail2(self):
        self.p1.go_to_jail()
        self.monopoly.jail_roll(6, 5)
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(1, self.p1.jail_turns_left)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.assertTrue(isinstance(self.p2.location.space, Housing))
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.assertTrue(isinstance(self.p3.location.space, Housing))
        self.monopoly.end_turn()
        self.monopoly.jail_roll(5, 5)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, FreeParking))

    def test_escape_jail3(self):
        self.p1.go_to_jail()
        self.monopoly.jail_roll(6, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.monopoly.end_turn()
        self.monopoly.jail_roll(5, 1)
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(0, self.p1.jail_turns_left)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p2.location.space, Housing))
        self.assertTrue(isinstance(self.p3.location.space, Utility))
        self.monopoly.jail_roll(5, 5)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, FreeParking))

    def test_escape_jail4_and_fp_payout(self):
        self.p1.go_to_jail()
        self.monopoly.jail_roll(6, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.monopoly.end_turn()
        self.monopoly.jail_roll(5, 1)
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(0, self.p1.jail_turns_left)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p2.location.space, Housing))
        self.assertTrue(isinstance(self.p3.location.space, Utility))
        self.monopoly.jail_roll(5, 3)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, Housing))
        self.assertEqual(1450, self.p1.balance)
        self.assertEqual(50, self.monopoly.free_parking_node.space.balance)
        self.monopoly.roll(1, 1)
        self.monopoly.end_turn()
        self.assertEqual(1550, self.p2.balance)
        self.assertEqual(0, self.monopoly.free_parking_node.space.balance)

    def test_bail_after_rolling(self):
        self.p1.go_to_jail()
        self.monopoly.jail_roll(6, 5)
        self.monopoly.bail()
        self.monopoly.end_turn()
        self.assertFalse(self.p1.in_jail)
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.monopoly.roll(5, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.assertTrue(isinstance(self.p1.location.space, Housing))

    def test_luxury_tax(self):
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 2)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, LuxuryTax))
        self.assertEqual(1425, self.p1.balance)
        self.assertEqual(75, self.monopoly.free_parking_node.space.balance)
        self.monopoly.roll(4, 5)
        self.monopoly.end_turn()
        self.assertEqual(1575, self.p2.balance)
        self.assertEqual(0, self.monopoly.free_parking_node.space.balance)

    def test_income_tax_default(self):
        self.monopoly.roll(3, 1)
        self.assertEqual(1350, self.p1.balance)
        self.assertEqual(150, self.monopoly.free_parking_node.space.balance)

    def test_tax_the_rich(self):
        self.p1.balance = 5000
        self.monopoly.roll(3, 1)
        self.assertEqual(4800, self.p1.balance)
        self.assertEqual(200, self.monopoly.free_parking_node.space.balance)

    def test_pass_go(self):
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        self.assertEqual(1700, self.p1.balance)

    def test_land_on_go(self):
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 3)
        self.monopoly.end_turn()
        self.assertEqual(1700, self.p1.balance)

    def test_buy_and_mortgage_baltic(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.assertEqual(1440, self.p1.balance)
        self.assertEqual(self.p1, self.p1.location.space.owner)
        self.assertEqual(1, len(self.p1.properties))
        self.assertEqual(4, self.p1.location.space.rent)
        self.assertEqual(1500, self.p1.calculate_net_worth())
        self.p1.player_mortgage("Baltic Avenue")
        self.assertTrue(self.p1.location.space.mortgaged)
        self.assertEqual(1470, self.p1.balance)
        self.assertEqual(1500, self.p1.calculate_net_worth())
        self.monopoly.end_turn()
        self.monopoly.roll(1, 2)
        self.monopoly.end_turn()
        self.assertEqual(1470, self.p1.balance)
        self.assertEqual(1500, self.p2.balance)


if __name__ == '__main__':
    unittest.main()
