import unittest
from gamemodel.monopolygame import MonopolyGame
from gamemodel.player import Player, Piece
from gamemodel.go import Go
from gamemodel.jail import Jail
from gamemodel.freeparking import FreeParking
from gamemodel.properties import Housing
from gamemodel.properties import Utility
from gamemodel.tax import LuxuryTax
from gamemodel.deed import *


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

    def test_use_baltic(self):
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
        self.p1.player_un_mortgage("Baltic Avenue")
        self.assertEqual(1437, self.p1.balance)
        self.assertEqual(1497, self.p1.calculate_net_worth())
        self.assertFalse(self.p1.location.space.mortgaged)
        self.monopoly.roll(1, 2)
        self.monopoly.end_turn()
        self.assertEqual(1441, self.p1.balance)
        self.assertEqual(1496, self.p3.balance)

    def test_get_brown_monopoly_and_use(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.build_houses("Mediterranean Avenue", 1)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(1, prop.houses)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(0, prop.houses)
        self.p1.build_houses("Baltic Avenue", 2)
        self.p1.build_houses("Mediterranean Avenue", 2)
        self.p1.build_houses("Baltic Avenue", 2)
        self.p1.build_houses("Mediterranean Avenue", 1)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.houses)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(4, prop.houses)

        self.assertEqual(24, self.p1.property_manager.houses)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(160, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(320, prop.rent)

        self.p1.build_hotel("Mediterranean Avenue")
        self.p1.build_hotel("Baltic Avenue")

        self.assertEqual(32, self.p1.property_manager.houses)
        self.assertEqual(10, self.p1.property_manager.hotels)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(250, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(450, prop.rent)

        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(5, 5)
            self.monopoly.end_turn()

        self.assertEqual(1450, self.p2.balance)
        self.assertEqual(1330, self.p1.balance)

        self.p1.sell_hotel("Baltic Avenue")
        self.assertEqual(1355, self.p1.balance)
        self.p1.sell_hotel("Mediterranean Avenue")
        self.assertEqual(1380, self.p1.balance)
        self.assertEqual(160, self.p2.location.space.rent)
        for i in range(4):
            self.p1.sell_houses("Mediterranean Avenue", 1)
            self.p1.sell_houses("Baltic Avenue", 1)
            self.assertEqual(1380 + (50 * (i + 1)), self.p1.balance)
        self.assertEqual(4, self.p2.location.space.rent)

    def test_roll_again_exception(self):
        with self.assertRaises(Exception):
            self.monopoly.roll(6, 4)
            self.monopoly.roll(6, 4)

    def test_buy_property_as_brokie(self):
        with self.assertRaises(Exception):
            self.p1.balance = 0
            self.monopoly.roll(5, 4)
            self.p1.purchase_location()

    def test_bankrupt_exception(self):
        with self.assertRaises(Exception):
            self.p1.declare_bankruptcy()

    def test_declare_bankruptcy_results(self):
        self.p2.balance = 1
        self.monopoly.roll(5, 4)
        self.p1.purchase_location()
        self.assertEqual(1380, self.p1.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.assertEqual(1381, self.p1.balance)
        self.p2.balance = 1
        self.p2.declare_bankruptcy()
        self.assertEqual(1382, self.p1.balance)
        self.monopoly.end_turn()
        self.assertEqual(2, len(self.monopoly.active_players))

    def test_cant_end_turn_in_debt(self):
        self.p2.balance = 1
        self.monopoly.roll(5, 4)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        with self.assertRaises(Exception):
            self.monopoly.end_turn()

    def test_pay_debt(self):
        self.p2.balance = 1
        self.monopoly.roll(5, 4)
        self.p1.purchase_location()
        self.assertEqual(1380, self.p1.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.assertEqual(1381, self.p1.balance)
        self.p2.balance = 100
        self.p2.pay_debt()
        self.assertEqual(1388, self.p1.balance)
        self.assertEqual(93, self.p2.balance)
        self.monopoly.end_turn()
        self.assertEqual(3, len(self.monopoly.active_players))

    def test_land_on_free_parking(self):
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(0, self.monopoly.free_parking_node.space.balance)
        self.monopoly.roll(2, 2)
        self.monopoly.end_turn()
        self.assertEqual(1350, self.p1.balance)
        self.assertEqual(150, self.monopoly.free_parking_node.space.balance)
        self.monopoly.roll(3, 3)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(0, self.monopoly.free_parking_node.space.balance)
        self.monopoly.end_turn()

    def test_advance_to_boardwalk_chance(self):
        self.assertEqual("Advance to Boardwalk.", Chance.cards[0].message)
        self.monopoly.roll(5, 2)
        self.assertEqual("Boardwalk", self.p1.location.space.name)
        self.assertEqual("Advance to Boardwalk.", Chance.cards[15].message)
        self.assertEqual("Advance to St. Charles Place. If you pass \"Go\" collect $200.", Chance.cards[0].message)

    def test_advance_to_st_charles_while_passing_go_chance(self):
        while Chance.cards[0].message != "Advance to St. Charles Place. If you pass \"Go\" collect $200.":
            Chance.cards.rotate(-1)
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual("Advance to St. Charles Place. If you pass \"Go\" collect $200.", Chance.cards[0].message)
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(3, 1)
        self.assertEqual(1700, self.p1.balance)
        self.assertEqual("St. Charles Place", self.p1.location.space.name)

    def test_three_doubles_doesnt_land_chance(self):
        while Chance.cards[0].message != "Advance to Boardwalk.":
            Chance.cards.rotate(1)
        self.assertEqual("Advance to Boardwalk.", Chance.cards[0].message)
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.monopoly.end_turn()
        self.assertEqual("Advance to Boardwalk.", Chance.cards[0].message)
        self.assertEqual("Jail", self.p1.location.space.name)

    def test_go_back_three_chance(self):
        while Chance.cards[0].message != "Go back three spaces.":
            Chance.cards.rotate(-1)
        self.assertEqual("Go back three spaces.", Chance.cards[0].message)
        self.monopoly.roll(5, 2)
        self.assertEqual("Income Tax", self.p1.location.space.name)

    def test_advance_to_nearest_railroad_chance(self):
        while Chance.cards[0].message != "Advance to the nearest railroad. If unowned, you " \
                                         "may buy it from the bank. If owned, pay the owner twice the rental to " \
                                         "which they are otherwise entitled.":
            Chance.cards.rotate(-1)
        self.assertEqual("Advance to the nearest railroad. If unowned, you may buy it from the bank. "
                         "If owned, pay the owner twice the rental to which they are otherwise entitled.",
                         Chance.cards[0].message)
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(3, 2)
        self.p1.purchase_location()
        self.assertEqual(self.p1, self.p1.location.space.owner)
        self.assertEqual(1300, self.p1.balance)
        self.assertEqual(25, self.p1.location.space.rent)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 2)
        self.monopoly.end_turn()
        self.assertEqual(self.p1.location, self.p2.location)
        self.assertEqual(1350, self.p1.balance)
        self.assertEqual(1450, self.p2.balance)
        self.assertEqual(False, self.p2.rent_multiplier)

    def test_buy_all_railroads(self):
        self.monopoly.roll(4, 1)
        self.p1.purchase_location()
        self.assertEqual(25, self.p1.location.space.rent)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.p1.purchase_location()
        self.assertEqual(50, self.p1.location.space.rent)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.p1.purchase_location()
        self.assertEqual(100, self.p1.location.space.rent)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.p1.purchase_location()
        self.assertEqual(200, self.p1.location.space.rent)
        self.monopoly.end_turn()
        self.p1.player_mortgage("Reading Railroad")
        self.assertEqual(200, self.p1.location.space.rent)
        self.p1.player_mortgage("Pennsylvania Railroad")
        self.assertEqual(200, self.p1.location.space.rent)
        self.p1.player_mortgage("B&O Railroad")
        self.assertEqual(200, self.p1.location.space.rent)
        self.p1.player_mortgage("Short Line")
        self.assertEqual(200, self.p1.location.space.rent)

    def test_advance_to_nearest_utility_chance_and_use_utilities(self):
        while Chance.cards[0].message != "Advance to the nearest utility. If unowned, you may buy it from the bank." \
                                         "If owned, throw dice and pay owner a total ten times amount thrown.":
            Chance.cards.rotate(-1)
        self.assertEqual("Advance to the nearest utility. If unowned, you may buy it from the bank."
                         "If owned, throw dice and pay owner a total ten times amount thrown.",
                         Chance.cards[0].message)
        self.assertEqual(1500, self.p1.balance)
        self.assertEqual(1500, self.p2.balance)
        self.assertEqual(1500, self.p3.balance)
        self.monopoly.roll(6, 6)
        self.p1.purchase_location()
        self.assertEqual(1350, self.p1.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 2)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.assertEqual(1398, self.p1.balance)
        self.assertEqual(1452, self.p2.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 2)
        self.monopoly.end_turn()
        self.monopoly.roll(3, 4)
        self.assertEqual(1468, self.p1.balance)
        self.assertEqual(1430, self.p3.balance)
        self.assertEqual(False, self.p3.rent_multiplier)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.assertEqual(1318, self.p1.balance)
        self.assertEqual(1452, self.p2.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 2)
        self.assertEqual(1348, self.p1.balance)
        self.assertEqual(1422, self.p2.balance)

    def test_invalid_dice_roll(self):
        with self.assertRaises(Exception):
            self.monopoly.roll(-1, 7)

    def test_try_to_roll_in_jail(self):
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.assertTrue(isinstance(self.p1.location.space, Jail))
        self.monopoly.roll(6, 4)
        self.assertTrue(isinstance(self.p2.location.space, Jail))
        self.monopoly.end_turn()
        self.monopoly.roll(4, 6)
        self.assertTrue(isinstance(self.p3.location.space, Jail))
        self.monopoly.end_turn()
        with self.assertRaises(Exception):
            self.monopoly.roll(2, 1)

    def test_end_turn_before_rolling(self):
        with self.assertRaises(Exception):
            self.monopoly.end_turn()

    def test_bail_while_not_in_jail(self):
        with self.assertRaises(Exception):
            self.monopoly.bail()

    def test_jail_roll_after_rolling(self):
        self.monopoly.roll(6, 4)
        with self.assertRaises(Exception):
            self.monopoly.jail_roll(3, 6)

    def test_invalid_jail_roll(self):
        with self.assertRaises(Exception):
            self.monopoly.jail_roll(-1, 7)

    def test_not_in_jail_jail_roll(self):
        with self.assertRaises(Exception):
            self.monopoly.jail_roll(1, 4)

    def test_starting_string(self):
        self.assertEqual(str(self.monopoly), "Dan : Go\nChris : Go\nLucas : Go\n")

    def test_linked_list_string(self):
        self.assertEqual(str(self.monopoly.board), 'Go ->\n'
                                                   'Mediterranean Avenue ->\n'
                                                   'Community Chest ->\n'
                                                   'Baltic Avenue ->\n'
                                                   'Income Tax ->\n'
                                                   'Reading Railroad ->\n'
                                                   'Oriental Avenue ->\n'
                                                   'Chance ->\n'
                                                   'Vermont Avenue ->\n'
                                                   'Connecticut Avenue ->\n'
                                                   'Jail ->\n'
                                                   'St. Charles Place ->\n'
                                                   'Electric Company ->\n'
                                                   'States Avenue ->\n'
                                                   'Virginia Avenue ->\n'
                                                   'Pennsylvania Railroad ->\n'
                                                   'St. James Place ->\n'
                                                   'Community Chest ->\n'
                                                   'Tennessee Avenue ->\n'
                                                   'New York Avenue ->\n'
                                                   'Free Parking ->\n'
                                                   'Kentucky Avenue ->\n'
                                                   'Chance ->\n'
                                                   'Indiana Avenue ->\n'
                                                   'Illinois Avenue ->\n'
                                                   'B&O Railroad ->\n'
                                                   'Atlantic Avenue ->\n'
                                                   'Ventnor Avenue ->\n'
                                                   'Water Works ->\n'
                                                   'Marvin Gardens ->\n'
                                                   'Go to Jail ->\n'
                                                   'Pacific Avenue ->\n'
                                                   'North Carolina Avenue ->\n'
                                                   'Community Chest ->\n'
                                                   'Pennsylvania Avenue ->\n'
                                                   'Short Line ->\n'
                                                   'Chance ->\n'
                                                   'Park Place ->\n'
                                                   'Luxury Tax ->\n'
                                                   'Boardwalk')

    def test_get_into_debt_while_owning_property_and_liquidate(self):
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 4)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.assertEqual(1, len(self.p1.properties))
        self.assertEqual(1300, self.p1.balance)
        self.monopoly.roll(3, 3)
        self.p2.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.p2.purchase_location()
        self.assertEqual(1240, self.p2.balance)
        self.p2.balance = 0
        self.monopoly.end_turn()
        self.monopoly.roll(3, 2)
        self.p2.liquidate_everything()
        self.assertEqual(130, self.p2.balance)
        self.p2.pay_debt()
        self.assertEqual(114, self.p2.balance)
        self.assertEqual(1316, self.p1.balance)
        self.monopoly.end_turn()

    def test_declare_bankruptcy_when_you_have_property(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.p1.balance = 0
        self.monopoly.end_turn()
        self.monopoly.roll(2, 3)
        self.p2.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.assertTrue(self.p1.debt > self.p1.balance)
        with self.assertRaises(Exception):
            self.p1.declare_bankruptcy()

    def test_try_to_pay_debt_when_not_in_debt(self):
        with self.assertRaises(Exception):
            self.p1.pay_debt()

    def test_try_to_pay_debt_but_not_enough(self):
        self.monopoly.roll(3, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.p2.balance = 0
        self.monopoly.roll(3, 2)
        with self.assertRaises(Exception):
            self.p2.pay_debt()

    def test_mortgaging_monopoly(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.player_mortgage("Mediterranean Avenue")

        self.assertEqual(1610, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
                self.assertTrue(prop.mortgaged)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)
                self.assertFalse(prop.mortgaged)

        self.p1.player_un_mortgage("Mediterranean Avenue")

        self.assertEqual(1577, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
                self.assertFalse(prop.mortgaged)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)
                self.assertFalse(prop.mortgaged)

        self.p1.build_houses("Mediterranean Avenue", 1)

        self.assertEqual(1527, self.p1.balance)

        self.p1.player_mortgage("Baltic Avenue")

        self.assertEqual(1557, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(10, prop.rent)
                self.assertFalse(prop.mortgaged)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)
                self.assertTrue(prop.mortgaged)

        with self.assertRaises(Exception):
            self.p1.player_mortgage("Mediterranean Avenue")

    def test_cant_afford_to_un_mortgage(self):
        self.monopoly.roll(3, 2)
        self.p1.purchase_location()
        self.p1.player_mortgage("Reading Railroad")
        self.p1.balance = 109
        with self.assertRaises(Exception):
            self.p1.player_un_mortgage("Reading Railroad")

    def test_collect_from_community_chest(self):
        self.assertEqual(1500, self.p1.balance)
        while CommunityChest.cards[0].message != "Bank error in your favor. Collect $200.":
            CommunityChest.cards.rotate(-1)
        self.monopoly.roll(1, 1)
        self.assertEqual(1700, self.p1.balance)
        self.assertEqual("Community Chest", self.p1.location.space.name)

    def test_no_property_by_that_name(self):
        with self.assertRaises(Exception):
            self.p1.player_mortgage("a")

    def test_cant_buy_space_that_is_not_property(self):
        with self.assertRaises(Exception):
            self.p1.purchase_location()

    def test_try_to_purchase_already_owned_property(self):
        self.monopoly.roll(3, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(4, 1)
        with self.assertRaises(Exception):
            self.p2.purchase_location()

    def test_liquidate_hotels(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.build_houses("Mediterranean Avenue", 1)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(1, prop.houses)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(0, prop.houses)
        self.p1.build_houses("Baltic Avenue", 2)
        self.p1.build_houses("Mediterranean Avenue", 2)
        self.p1.build_houses("Baltic Avenue", 2)
        self.p1.build_houses("Mediterranean Avenue", 1)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.houses)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(4, prop.houses)

        self.assertEqual(24, self.p1.property_manager.houses)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(160, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(320, prop.rent)

        self.assertEqual(24, self.p1.property_manager.houses)
        self.assertEqual(12, self.p1.property_manager.hotels)

        self.p1.build_hotel("Mediterranean Avenue")
        self.p1.build_hotel("Baltic Avenue")

        self.assertEqual(32, self.p1.property_manager.houses)
        self.assertEqual(10, self.p1.property_manager.hotels)
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(250, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(450, prop.rent)

        self.assertEqual(1080, self.p1.balance)
        self.p1.liquidate_everything()
        self.assertEqual(32, self.p1.property_manager.houses)
        self.assertEqual(12, self.p1.property_manager.hotels)
        self.assertEqual(1390, self.p1.balance)

    def test_try_to_violate_one_house_difference(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        with self.assertRaises(Exception):
            self.p1.build_houses("Mediterranean Avenue", 2)

    def test_not_enough_houses_in_bank(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.monopoly.property_manager.houses = 0

        with self.assertRaises(Exception):
            self.p1.build_houses("Mediterranean Avenue", 1)

    def test_charge_each(self):
        self.assertEqual(1500, self.p1.balance)
        while CommunityChest.cards[0].message != "Grand Opera Night. Collect $50 from every player " \
                                                 "for opening night seats.":
            CommunityChest.cards.rotate(-1)
        self.monopoly.roll(1, 1)
        self.assertEqual(1600, self.p1.balance)
        self.assertEqual(1450, self.p2.balance)
        self.assertEqual(1450, self.p3.balance)

    def test_charge_each_debt_end_turn(self):
        self.assertEqual(1500, self.p1.balance)
        self.p3.balance = 10
        while CommunityChest.cards[0].message != "Grand Opera Night. Collect $50 from every player " \
                                                 "for opening night seats.":
            CommunityChest.cards.rotate(-1)
        self.monopoly.roll(1, 1)
        self.assertEqual(1560, self.p1.balance)
        with self.assertRaises(Exception):
            self.monopoly.end_turn()

    def test_pay_each(self):
        self.assertEqual(1500, self.p1.balance)
        while Chance.cards[0].message != "You have been elected chairman of the board. Pay each player $50":
            Chance.cards.rotate(-1)
        self.monopoly.roll(3, 4)
        self.assertEqual(1400, self.p1.balance)
        self.assertEqual(1550, self.p2.balance)
        self.assertEqual(1550, self.p3.balance)

    def test_pay_each_debt(self):
        self.p1.balance = 40
        while Chance.cards[0].message != "You have been elected chairman of the board. Pay each player $50":
            Chance.cards.rotate(-1)
        self.monopoly.roll(3, 4)
        self.assertEqual(0, self.p1.balance)
        self.assertEqual(1520, self.p2.balance)
        self.assertEqual(1520, self.p3.balance)
        self.p1.balance = 60
        self.p1.pay_debt()
        self.assertEqual(0, self.p1.balance)
        self.assertEqual(1550, self.p2.balance)
        self.assertEqual(1550, self.p3.balance)

    def test_declare_bankruptcy_with_multiple_debts(self):
        self.p1.balance = 40
        while Chance.cards[0].message != "You have been elected chairman of the board. Pay each player $50":
            Chance.cards.rotate(-1)
        self.monopoly.roll(3, 4)
        self.assertEqual(0, self.p1.balance)
        self.assertEqual(1520, self.p2.balance)
        self.assertEqual(1520, self.p3.balance)
        self.p1.balance = 40
        self.p1.declare_bankruptcy()
        self.assertEqual(0, self.p1.balance)
        self.assertEqual(1540, self.p2.balance)
        self.assertEqual(1540, self.p3.balance)
        self.monopoly.end_turn()
        self.assertEqual(2, len(self.monopoly.active_players))

    def test_repair_costs_with_no_buildings(self):
        self.assertEqual(1500, self.p1.balance)
        while Chance.cards[0].message != "Make general repairs on all you property: for each house pay " \
                                         "$25, for each hotel pay $100.":
            Chance.cards.rotate(-1)
        self.monopoly.roll(2, 5)
        self.assertEqual(1500, self.p1.balance)

    def test_repair_costs_with_buildings(self):
        self.p1.balance = 3000
        while Chance.cards[0].message != "Make general repairs on all you property: for each house pay " \
                                         "$25, for each hotel pay $100.":
            Chance.cards.rotate(-1)
        for i in range(2):
            self.monopoly.roll(6, 6)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 2)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(3, 3)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.p1.purchase_location()
        self.p1.build_houses("Park Place", 1)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 2)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 1)
        self.p1.build_hotel("Boardwalk")
        self.assertEqual(450, self.p1.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 3)
        self.assertEqual(450, self.p1.balance)
        self.assertEqual("Chance", self.p1.location.space.name)

    def test_three_dubs_doesnt_land(self):
        self.p1.balance = 3000
        while Chance.cards[0].message != "Make general repairs on all you property: for each house pay " \
                                         "$25, for each hotel pay $100.":
            Chance.cards.rotate(-1)
        for i in range(2):
            self.monopoly.roll(6, 6)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 2)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(3, 3)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.p1.purchase_location()
        self.p1.build_houses("Park Place", 1)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 2)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 1)
        self.p1.build_hotel("Boardwalk")
        self.assertEqual(450, self.p1.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.assertEqual(450, self.p1.balance)
        self.assertEqual("Jail", self.p1.location.space.name)
        self.assertEqual("Make general repairs on all you property: for each house pay "
                         "$25, for each hotel pay $100.", Chance.cards[0].message)

    def test_declare_bankruptcy_with_monopolies_and_properties(self):
        self.p1.balance = 3000
        for i in range(2):
            self.monopoly.roll(6, 6)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 2)
        self.monopoly.end_turn()
        self.monopoly.roll(3, 2)
        self.p2.purchase_location()
        self.assertEqual(1300, self.p2.balance)
        self.p2.location.space.rent = 10000
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(3, 3)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.p1.purchase_location()
        self.p1.build_houses("Park Place", 1)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 2)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 1)
        self.p1.build_hotel("Boardwalk")
        self.p1.build_hotel("Park Place")
        self.assertEqual(250, self.p1.balance)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 2)
        self.assertEqual(1750, self.p2.balance)
        self.assertEqual(9550, self.p1.debt)
        self.assertEqual(0, self.p1.balance)
        self.p1.liquidate_everything()
        self.assertEqual(1375, self.p1.balance)
        self.p1.declare_bankruptcy()
        self.assertEqual(0, self.p1.balance)
        self.assertEqual(0, len(self.p1.properties))
        self.assertEqual(3125, self.p2.balance)
        self.monopoly.end_turn()
        while CommunityChest.cards[0].message != "Grand Opera Night. Collect $50 from every player " \
                                                 "for opening night seats.":
            CommunityChest.cards.rotate(-1)
        self.monopoly.roll(6, 6)
        self.assertEqual(3175, self.p2.balance)
        self.assertEqual(1450, self.p3.balance)
        self.assertEqual("Community Chest", self.p2.location.space.name)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.assertEqual("Boardwalk", self.p2.location.space.name)
        self.assertEqual(None, self.p2.location.space.owner)
        self.assertEqual("Jail", self.p3.location.space.name)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 5)
        self.assertEqual("Park Place", self.p3.location.space.name)
        self.assertEqual(None, self.p3.location.space.owner)

    def test_chance_jail_free_card(self):
        self.assertEqual(16, len(Chance.cards))
        self.assertEqual(0, len(self.p1.jail_free_cards))
        while not isinstance(Chance.cards[0], GetOutOfJailFreeCard):
            Chance.cards.rotate(-1)
        self.monopoly.roll(3, 4)
        self.assertEqual(15, len(Chance.cards))
        self.assertEqual(1, len(self.p1.jail_free_cards))
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(3, 2)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.monopoly.bail()
        self.assertEqual(16, len(Chance.cards))
        self.assertEqual(0, len(self.p1.jail_free_cards))
        self.assertFalse(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.assertTrue(isinstance(Chance.cards[15], GetOutOfJailFreeCard))

    def test_community_chest_jail_free_card(self):
        self.assertEqual(16, len(CommunityChest.cards))
        self.assertEqual(0, len(self.p1.jail_free_cards))
        while not isinstance(CommunityChest.cards[0], GetOutOfJailFreeCard):
            CommunityChest.cards.rotate(-1)
        self.monopoly.roll(1, 1)
        self.assertEqual(15, len(CommunityChest.cards))
        self.assertEqual(1, len(self.p1.jail_free_cards))
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.monopoly.bail()
        self.assertEqual(16, len(CommunityChest.cards))
        self.assertEqual(0, len(self.p1.jail_free_cards))
        self.assertFalse(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.assertTrue(isinstance(CommunityChest.cards[15], GetOutOfJailFreeCard))

    def test_both_jail_free_cards(self):
        while not isinstance(CommunityChest.cards[0], GetOutOfJailFreeCard):
            CommunityChest.cards.rotate(-1)
        while not isinstance(Chance.cards[0], GetOutOfJailFreeCard):
            Chance.cards.rotate(-1)
        self.monopoly.roll(1, 1)
        self.assertEqual(15, len(CommunityChest.cards))
        self.assertEqual(1, len(self.p1.jail_free_cards))
        self.monopoly.end_turn()
        self.monopoly.roll(4, 1)
        self.assertEqual(15, len(Chance.cards))
        self.assertEqual(2, len(self.p1.jail_free_cards))
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(3, 2)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.assertTrue(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.monopoly.bail()
        self.assertEqual(16, len(CommunityChest.cards))
        self.assertEqual(15, len(Chance.cards))
        self.assertEqual(1, len(self.p1.jail_free_cards))
        self.assertEqual(CardType.CHANCE, self.p1.jail_free_cards[0].card_type)
        self.assertFalse(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.assertTrue(isinstance(CommunityChest.cards[15], GetOutOfJailFreeCard))
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(3, 1)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.assertEqual(1500, self.p1.balance)
        self.monopoly.bail()
        self.assertEqual(16, len(CommunityChest.cards))
        self.assertEqual(16, len(Chance.cards))
        self.assertEqual(0, len(self.p1.jail_free_cards))
        self.assertFalse(self.p1.in_jail)
        self.assertEqual(1500, self.p1.balance)
        self.assertTrue(isinstance(CommunityChest.cards[15], GetOutOfJailFreeCard))
        self.assertTrue(isinstance(Chance.cards[15], GetOutOfJailFreeCard))

    def test_roll_doubles_land_on_gtj(self):
        for i in range(3):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(5, 5)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.assertEqual("Free Parking", self.p2.location.space.name)

    def test_go_nearest_railroad_pass_go(self):
        while Chance.cards[0].message != "Advance to the nearest railroad. If unowned, you " \
                                         "may buy it from the bank. If owned, pay the owner twice the rental to " \
                                         "which they are otherwise entitled.":
            Chance.cards.rotate(-1)
        self.assertEqual("Advance to the nearest railroad. If unowned, you may buy it from the bank. "
                         "If owned, pay the owner twice the rental to which they are otherwise entitled.",
                         Chance.cards[0].message)
        for i in range(2):
            self.monopoly.roll(5, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(3, 2)
        self.assertEqual(1700, self.p1.balance)
        self.assertEqual("Reading Railroad", self.p1.location.space.name)

    def test_go_nearest_utility_pass_go(self):
        while Chance.cards[0].message != "Advance to the nearest utility. If unowned, you may buy it from the bank." \
                      "If owned, throw dice and pay owner a total ten times amount thrown.":
            Chance.cards.rotate(-1)
        self.assertEqual("Advance to the nearest utility. If unowned, you may buy it from the bank."
                         "If owned, throw dice and pay owner a total ten times amount thrown.",
                         Chance.cards[0].message)
        for i in range(2):
            self.monopoly.roll(5, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(3, 2)
        self.assertEqual(1700, self.p1.balance)
        self.assertEqual("Electric Company", self.p1.location.space.name)

    def test_try_to_mortgage_unowned_property(self):
        self.monopoly.roll(3, 2)
        with self.assertRaises(Exception):
            self.p1.location.space.prop_mortgage()

    def test_try_to_un_mortgage_unowned_property(self):
        self.monopoly.roll(3, 2)
        with self.assertRaises(Exception):
            self.p1.location.space.prop_un_mortgage()

    def test_try_to_mortgage_mortgaged_property(self):
        self.monopoly.roll(3, 2)
        self.p1.purchase_location()
        self.p1.player_mortgage("Reading Railroad")
        with self.assertRaises(Exception):
            self.p1.location.space.prop_mortgage()

    def test_try_to_un_mortgage_un_mortgaged_property(self):
        self.monopoly.roll(3, 2)
        self.p1.purchase_location()
        with self.assertRaises(Exception):
            self.p1.location.space.prop_un_mortgage()

    def test_cant_afford_house(self):
        while Chance.cards[0].message != "Make general repairs on all you property: for each house pay " \
                                         "$25, for each hotel pay $100.":
            Chance.cards.rotate(-1)
        for i in range(2):
            self.monopoly.roll(6, 6)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 2)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(3, 3)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.p1.purchase_location()
        self.p1.build_houses("Park Place", 1)
        self.p1.build_houses("Boardwalk", 2)
        with self.assertRaises(Exception):
            self.p1.build_houses("Park Place", 1)

    def test_cant_afford_hotel(self):
        self.p1.balance = 2400
        while Chance.cards[0].message != "Make general repairs on all you property: for each house pay " \
                                         "$25, for each hotel pay $100.":
            Chance.cards.rotate(-1)
        for i in range(2):
            self.monopoly.roll(6, 6)
            self.monopoly.end_turn()
        self.monopoly.roll(5, 2)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(3, 3)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.p1.purchase_location()
        self.p1.build_houses("Park Place", 1)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 2)
        self.p1.build_houses("Boardwalk", 2)
        self.p1.build_houses("Park Place", 1)
        with self.assertRaises(Exception):
            self.p1.build_hotel("Boardwalk")

    def test_try_to_reset_with_houses(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.build_houses("Mediterranean Avenue", 1)

        with self.assertRaises(Exception):
            self.p1.location.space.reset()

    def test_reset_railroads(self):
        for i in range(3):
            self.monopoly.roll(1, 4)
            self.monopoly.end_turn()
        self.p1.purchase_location()
        self.monopoly.roll(4, 6)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(1, 4)
        self.monopoly.end_turn()
        self.p2.purchase_location()
        self.p2.location.space.rent = 999999
        self.monopoly.roll(3, 2)
        self.monopoly.end_turn()
        railroads = self.p1.properties.copy()
        for prop in railroads:
            self.assertEqual(self.p1, prop.owner)
            self.assertEqual(50, prop.rent)
        self.monopoly.roll(2, 1)
        self.p1.player_mortgage("Reading Railroad")
        self.p1.player_mortgage("Pennsylvania Railroad")
        self.p1.declare_bankruptcy()
        self.assertEqual(0, len(self.p1.properties))
        self.assertEqual(2, len(railroads))
        for prop in railroads:
            self.assertEqual(None, prop.owner)
            self.assertEqual(25, prop.rent)

    def test_reset_utilities(self):
        self.monopoly.roll(6, 6)
        self.p1.purchase_location()
        self.assertFalse(self.p1.location.space.both_owned)
        self.monopoly.end_turn()
        self.monopoly.roll(4, 4)
        self.monopoly.end_turn()
        self.monopoly.roll(2, 6)
        self.p1.purchase_location()
        self.assertTrue(self.p1.location.space.both_owned)
        self.assertEqual(2, len(self.p1.properties))
        utilities = self.p1.properties.copy()
        for prop in utilities:
            self.assertEqual(self.p1, prop.owner)
            self.assertTrue(prop.both_owned)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(5, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 5)
        self.p2.purchase_location()
        self.monopoly.end_turn()
        self.p2.location.space.rent = 999999
        self.monopoly.roll(3, 2)
        self.monopoly.end_turn()
        self.monopoly.roll(2, 1)
        self.p1.player_mortgage("Electric Company")
        self.p1.player_mortgage("Water Works")
        self.p1.declare_bankruptcy()
        self.assertEqual(0, len(self.p1.properties))
        self.assertEqual(2, len(utilities))
        for prop in utilities:
            self.assertEqual(None, prop.owner)
            self.assertFalse(prop.both_owned)

    def test_claim_none(self):
        self.monopoly.roll(1, 2)
        with self.assertRaises(Exception):
            self.monopoly.property_manager.claim(self.p1.location.space, None)

    def test_claim_what_you_already_own(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        with self.assertRaises(Exception):
            self.monopoly.property_manager.claim(self.p1.location.space, self.p1)

    def test_claim_when_buildings_in_group(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.build_houses("Baltic Avenue", 1)

        with self.assertRaises(Exception):
            self.monopoly.property_manager.claim(self.p1.location.space, self.p2)

    def test_claim_when_buildings_on_it(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.build_houses("Mediterranean Avenue", 1)

        with self.assertRaises(Exception):
            self.monopoly.property_manager.claim(self.p1.location.space, self.p2)

    def test_build_without_monopoly(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        with self.assertRaises(Exception):
            self.p1.build_houses("Baltic Avenue", 1)

    def test_build_house_with_hotel_already_present(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.p1.build_hotel("Mediterranean Avenue")
        self.p1.build_hotel("Baltic Avenue")

        with self.assertRaises(Exception):
            self.p1.build_houses("Mediterranean Avenue", 1)

    def test_build_hotel_with_hotel_already_present(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.p1.build_hotel("Mediterranean Avenue")
        with self.assertRaises(Exception):
            self.p1.build_hotel("Mediterranean Avenue")

    def test_build_hotel_with_not_enough_houses(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(3):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.p1.build_houses("Mediterranean Avenue", 1)

        with self.assertRaises(Exception):
            self.p1.build_hotel("Mediterranean Avenue")

    def test_not_enough_hotels(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.monopoly.property_manager.hotels = 0

        with self.assertRaises(Exception):
            self.p1.build_hotel("Mediterranean Avenue")

    def test_sell_too_many_houses(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        with self.assertRaises(Exception):
            self.p1.sell_houses("Baltic Avenue", 5)

    def test_sell_houses_when_hotel_present(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.p1.build_hotel("Baltic Avenue")

        with self.assertRaises(Exception):
            self.p1.sell_houses("Mediterranean Avenue", 1)

    def test_sell_houses_violate_one_building_difference(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.assertEqual(1180, self.p1.balance)
        self.p1.sell_houses("Baltic Avenue", 2)
        self.assertEqual(1230, self.p1.balance)

    def test_no_hotel_to_sell(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        with self.assertRaises(Exception):
            self.p1.sell_hotel("Baltic Avenue")

    def test_reset_with_no_owner(self):
        self.monopoly.roll(1, 2)
        with self.assertRaises(Exception):
            self.monopoly.property_manager.reset(self.p1.location.space)

    def test_build_houses_when_mortgaged(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.player_mortgage("Baltic Avenue")

        self.p1.build_houses("Mediterranean Avenue", 1)
        self.assertEqual(1, self.p1.location.space.houses)

        with self.assertRaises(Exception):
            self.p1.build_houses("Baltic Avenue", 1)

    def test_build_negative_houses(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.player_mortgage("Baltic Avenue")

        with self.assertRaises(ValueError):
            self.p1.build_houses("Mediterranean Avenue", -1)

    def test_build_too_many_houses(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)

        self.p1.player_mortgage("Baltic Avenue")

        with self.assertRaises(Exception):
            self.p1.build_houses("Mediterranean Avenue", 6)

    def test_sell_hotel_get_no_houses_back(self):
        self.monopoly.roll(1, 2)
        self.p1.purchase_location()
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 4)
            self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 6)
        self.monopoly.end_turn()
        self.monopoly.roll(6, 4)
        self.monopoly.end_turn()
        for i in range(2):
            self.monopoly.roll(6, 5)
            self.monopoly.end_turn()
        self.monopoly.roll(1, 3)
        self.p1.purchase_location()
        self.assertEqual(1580, self.p1.balance)
        self.assertEqual(2, len(self.p1.properties))
        for prop in self.p1.properties:
            if prop.name == "Mediterranean Avenue":
                self.assertEqual(4, prop.rent)
            elif prop.name == "Baltic Avenue":
                self.assertEqual(8, prop.rent)
        for i in range(4):
            self.p1.build_houses("Mediterranean Avenue", 1)
            self.p1.build_houses("Baltic Avenue", 1)

        self.p1.build_hotel("Mediterranean Avenue")
        self.monopoly.property_manager.houses = 0
        self.p1.sell_hotel("Mediterranean Avenue")

        self.assertEqual(0, self.p1.location.space.houses)
        self.assertEqual(4, self.p1.location.space.rent)

    def test_declare_bankruptcy_with_jail_free_card(self):
        while not isinstance(CommunityChest.cards[0], GetOutOfJailFreeCard):
            CommunityChest.cards.rotate(-1)
        self.monopoly.roll(3, 6)
        self.p1.purchase_location()
        self.p1.location.space.rent = 99999
        self.monopoly.end_turn()
        self.monopoly.roll(1, 1)
        self.assertEqual(15, len(CommunityChest.cards))
        self.assertEqual(1, len(self.p2.jail_free_cards))
        self.monopoly.end_turn()
        self.monopoly.roll(4, 3)
        self.p2.declare_bankruptcy()
        self.assertEqual(16, len(CommunityChest.cards))
        self.assertEqual(0, len(self.p2.jail_free_cards))
        self.assertTrue(isinstance(CommunityChest.cards[15], GetOutOfJailFreeCard))


if __name__ == '__main__':
    unittest.main()
