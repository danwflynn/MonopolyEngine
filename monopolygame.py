from typing import List
import random

from go import Go
from player import Player
from properties import *
from deedcard import *
from tax import *
from jail import *
from freeparking import FreeParking
from spaceslinkedlist import CircularLinkedList
from propertymanager import PropertyManager


class MonopolyGame:
    def __init__(self, players: List[Player]):
        self.players = deque(players)
        self.board = CircularLinkedList()
        self.doubles_in_a_row = 0
        self.roll_available = True
        self.property_manager = PropertyManager()

        self.board.append(Go())
        self.board.append(Housing("Mediterranean Avenue", 60, 30, Color.BROWN, 50, (2, 10, 30, 90, 160, 250)))
        self.board.append(CommunityChest(self))
        self.board.append(Housing("Baltic Avenue", 60, 30, Color.BROWN, 50, (4, 20, 60, 180, 320, 450)))
        self.board.append(IncomeTax(self))
        self.board.append(Railroad("Reading Railroad"))
        self.board.append(Housing("Oriental Avenue", 100, 50, Color.LIGHT_BLUE, 50, (6, 30, 90, 270, 400, 550)))
        self.board.append(Chance(self))
        self.board.append(Housing("Vermont Avenue", 100, 50, Color.LIGHT_BLUE, 50, (6, 30, 90, 270, 400, 550)))
        self.board.append(Housing("Connecticut Avenue", 120, 60, Color.LIGHT_BLUE, 50, (8, 40, 100, 300, 450, 600)))
        self.board.append(Jail())
        self.board.append(Housing("St. Charles Place", 140, 70, Color.MAGENTA, 100, (10, 50, 150, 450, 625, 750)))
        self.board.append(ElectricCompany())
        self.board.append(Housing("States Avenue", 140, 70, Color.MAGENTA, 100, (10, 50, 150, 450, 625, 750)))
        self.board.append(Housing("Virginia Avenue", 160, 80, Color.MAGENTA, 100, (12, 60, 180, 500, 700, 900)))
        self.board.append(Railroad("Pennsylvania Railroad"))
        self.board.append(Housing("St. James Place", 180, 90, Color.ORANGE, 100, (14, 70, 200, 550, 750, 950)))
        self.board.append(CommunityChest(self))
        self.board.append(Housing("Tennessee Avenue", 180, 90, Color.ORANGE, 100, (14, 70, 200, 550, 750, 950)))
        self.board.append(Housing("New York Avenue", 200, 100, Color.ORANGE, 100, (16, 80, 220, 600, 800, 1000)))
        self.board.append(FreeParking())
        self.board.append(Housing("Kentucky Avenue", 220, 110, Color.RED, 150, (18, 90, 250, 700, 875, 1050)))
        self.board.append(Chance(self))
        self.board.append(Housing("Indiana Avenue", 220, 110, Color.RED, 150, (18, 90, 250, 700, 875, 1050)))
        self.board.append(Housing("Illinois Avenue", 240, 120, Color.RED, 150, (20, 100, 300, 750, 925, 1100)))
        self.board.append(Railroad("B&O Railroad"))
        self.board.append(Housing("Atlantic Avenue", 260, 130, Color.YELLOW, 150, (22, 110, 330, 800, 975, 1150)))
        self.board.append(Housing("Ventnor Avenue", 260, 130, Color.YELLOW, 150, (22, 110, 330, 800, 975, 1150)))
        self.board.append(WaterWorks())
        self.board.append(Housing("Marvin Gardens", 280, 140, Color.YELLOW, 150, (24, 120, 360, 850, 1025, 1200)))
        self.board.append(GoToJail())
        self.board.append(Housing("Pacific Avenue", 300, 150, Color.GREEN, 200, (26, 130, 390, 900, 1100, 1275)))
        self.board.append(Housing("North Carolina Avenue", 300, 150, Color.GREEN, 200, (26, 130, 390, 900, 1100, 1275)))
        self.board.append(CommunityChest(self))
        self.board.append(Housing("Pennsylvania Avenue", 320, 160, Color.GREEN, 200, (28, 150, 450, 1000, 1200, 1400)))
        self.board.append(Railroad("Short Line"))
        self.board.append(Chance(self))
        self.board.append(Housing("Park Place", 350, 175, Color.DARK_BLUE, 200, (35, 175, 500, 1100, 1300, 1500)))
        self.board.append(LuxuryTax(self))
        self.board.append(Housing("Boardwalk", 400, 200, Color.DARK_BLUE, 200, (50, 200, 600, 1400, 1700, 2000)))

        for player in self.players:
            player.location = self.board.head

        temp = self.board.head
        for i in range(39):
            temp = temp.next
            if isinstance(temp.space, Housing):
                if temp.space.color in self.property_manager.monopoly_color_groups:
                    self.property_manager.monopoly_color_groups[temp.space.color].append(temp.space)
                else:
                    self.property_manager.monopoly_color_groups[temp.space.color] = [temp.space]

        for player in self.players:
            player.property_manager = self.property_manager
            self.property_manager.railroad_owners[player] = []
            self.property_manager.utility_owners[player] = []

        self.free_parking_node = self.board.head
        while not isinstance(self.free_parking_node.space, FreeParking):
            self.free_parking_node = self.free_parking_node.next

    def __move_acting_player(self, n: int):
        for i in range(n):
            self.players[0].location = self.players[0].location.next
            if isinstance(self.players[0].location.space, Go):
                self.players[0].balance += 200
        self.players[0].land()

    def roll(self, die1=random.randint(1, 6), die2=random.randint(1, 6)):
        if not self.roll_available:
            raise Exception("Already rolled for this turn")
        if die1 < 1 or die1 > 6 or die2 < 1 or die2 > 6:
            raise ValueError("Invalid dice roll")
        if self.players[0].in_jail:
            raise Exception("Can't use roll function while in jail. Use jail_roll, goojfc or bail instead.")
        self.roll_available = False
        self.players[0].last_roll = die1 + die2
        if die1 == die2:
            self.doubles_in_a_row += 1
        else:
            self.doubles_in_a_row = 0
        if self.doubles_in_a_row == 3:
            self.doubles_in_a_row = 0
            self.players[0].go_to_jail()
            return
        self.__move_acting_player(die1 + die2)

    def end_turn(self):
        if self.players[0].debt != 0:
            raise Exception("Can't end turn when the acting player is in debt")
        if self.doubles_in_a_row == 0:
            self.players.rotate(-1)
        self.roll_available = True

    def bail(self):
        if not self.players[0].in_jail:
            raise Exception("Can't bail someone out who isn't in jail")
        self.players[0].charge(50, self.free_parking_node.space)
        self.players[0].in_jail = False
        self.players[0].jail_turns_left = 0

    def jail_roll(self, die1=random.randint(1, 6), die2=random.randint(1, 6)):
        if not self.roll_available:
            raise Exception("Already rolled for this turn")
        if die1 < 1 or die1 > 6 or die2 < 1 or die2 > 6:
            raise ValueError("Invalid dice roll")
        if not self.players[0].in_jail:
            raise Exception("Can't use jail_roll when not in jail")
        self.roll_available = False
        if die1 == die2:
            self.players[0].in_jail = False
            self.players[0].jail_turns_left = 0
            self.__move_acting_player(die1 + die2)
        elif self.players[0].jail_turns_left > 0:
            self.players[0].jail_turns_left -= 1
        else:
            self.bail()
            self.__move_acting_player(die1 + die2)

    def __str__(self):
        result = ""
        for p in self.players:
            result += p.name + " : " + p.location.space.name + "\n"
        return result
