from gamemodel.properties import *
from gamemodel.player import Player
from typing import List


class PropertyManager:
    def __init__(self):
        self.houses = 32
        self.hotels = 12
        self.monopoly_color_groups = {}
        self.railroad_owners = {}
        self.utility_owners = {}

    def claim(self, prop: Property, player: Player):
        if player is None:
            raise Exception("Player can't be null")
        if prop.owner is player:
            raise Exception("Cannot claim what you already own")
        old_owner = prop.owner
        prop.owner = player
        player.properties.append(prop)
        if isinstance(prop, Housing):
            buildings = sum([x.houses for x in self.monopoly_color_groups[prop.color]]) \
                    + sum([x.hotels for x in self.monopoly_color_groups[prop.color]])
            if buildings != 0:
                raise Exception(f'Cannot claim {prop.name} when there are {buildings} (not 0) buildings in its group')
            if len(set([x.owner for x in self.monopoly_color_groups[prop.color]])) == 1:
                for p in self.monopoly_color_groups[prop.color]:
                    if p.rent == p.rents[0]:
                        p.rent *= 2
            else:
                for p in self.monopoly_color_groups[prop.color]:
                    p.rent = p.rents[0]
        elif isinstance(prop, Railroad):
            self.railroad_owners[player].append(prop)
            if old_owner is not None:
                self.railroad_owners[old_owner].remove(prop)
            for railroad in self.railroad_owners[player]:
                railroad.rent = 25 * (2 ** (len(self.railroad_owners[player]) - 1))
            if old_owner is not None:
                for railroad in self.railroad_owners[old_owner]:
                    railroad.rent = 25 * (2 ** (len(self.railroad_owners[old_owner]) - 1))
        else:
            self.utility_owners[player].append(prop)
            if old_owner is not None:
                self.utility_owners[old_owner].remove(prop)
            for utility in self.utility_owners[player]:
                utility.both_owned = len(self.utility_owners[player]) == 2
            for utility in self.utility_owners[old_owner]:
                utility.both_owned = len(self.utility_owners[old_owner]) == 2

    def claim_monopoly(self, monopoly: List[Housing], player: Player):
        if len(set([prop.color for prop in monopoly])) != 1:
            raise Exception("Can't have more that 1 color in a monopoly")
        if len(monopoly) != len(self.monopoly_color_groups[monopoly[0]]):
            raise Exception("Number of properties in the list is wrong")
        if len(set([x.owner for x in self.monopoly_color_groups[monopoly[0].color]])) != 1:
            raise Exception("Not a monopoly")
        for prop in monopoly:
            prop.owner = player

    def build_houses(self, prop: Housing, n: int):
        if len(set([x.owner for x in self.monopoly_color_groups[prop.color]])) != 1:
            raise Exception(prop.name + " is not monopolized")
        if prop.hotels != 0:
            raise Exception(prop.name + " has a hotel")
        if n < 1:
            raise ValueError("Can't buy <= 0 houses")
        if prop.houses + n > 4:
            raise Exception("Max house amount is 4")
        if prop.owner.balance < prop.building_cost:
            raise Exception("Can't afford house")
        if n > self.houses:
            raise Exception("Not enough houses in the bank")
        for p in self.monopoly_color_groups[prop.color]:
            if p.mortgaged:
                raise Exception(p + " is mortgaged")
        proposed_house_amounts = []
        for p in self.monopoly_color_groups[prop.color]:
            if p is prop:
                proposed_house_amounts.append(p.houses + n)
            else:
                proposed_house_amounts.append(p.houses)
        if max(proposed_house_amounts) - min(proposed_house_amounts) > 1:
            raise Exception("Properties in a monopoly can only have a 1 building difference")

        prop.owner.balance -= n * prop.building_cost
        prop.houses += n
        self.houses -= n
        prop.rent = prop.rents[prop.houses]

    def build_hotel(self, prop: Housing):
        if len(set([x.owner for x in self.monopoly_color_groups[prop.color]])) != 1 or prop.houses != 4 \
                or prop.hotels != 0:
            raise Exception(prop.name + " not eligible for hotel")
        for p in self.monopoly_color_groups[prop.color]:
            if p.houses != 4 and p.hotels != 1:
                raise Exception(f'{p.name} has {p.houses} houses which isn\'t the required 4')
        if prop.owner.balance < prop.building_cost:
            raise Exception("Can't afford hotel")
        if self.hotels < 1:
            raise Exception("No hotels remaining in the bank")
        prop.owner.balance -= prop.building_cost
        prop.hotels = 1
        prop.houses = 0
        self.houses += 4
        self.hotels -= 1
        prop.rent = prop.rents[5]

    def sell_houses(self, prop: Housing, n: int):
        if prop.houses < n:
            raise Exception(f'{prop.name} can\'t sell {n} houses')
        for p in self.monopoly_color_groups[prop.color]:
            if p.hotels:
                raise Exception(f'{p.name} has a hotel')
        proposed_house_amounts = []
        for p in self.monopoly_color_groups[prop.color]:
            if p is prop:
                proposed_house_amounts.append(p.houses - n)
            else:
                proposed_house_amounts.append(p.houses)
        if max(proposed_house_amounts) - min(proposed_house_amounts) > 1:
            raise Exception("Properties in a monopoly can only have a 1 building difference")
        prop.houses -= n
        prop.owner.balance += n * prop.building_cost // 2
        self.houses += n
        prop.rent = prop.rents[prop.houses]
        if prop.houses == 0:
            prop.rent = prop.rents[0] * 2

    def sell_hotel(self, prop: Housing):
        if prop.hotels < 1:
            raise Exception(prop.name + " has no hotel to sell")
        prop.hotels = 0
        prop.owner.balance += prop.building_cost // 2
        self.hotels += 1
        houses_back = min(4, self.houses)
        self.houses -= houses_back
        prop.houses = houses_back
        prop.owner.balance += (4 - houses_back) * prop.building_cost // 2
        prop.rent = prop.rents[prop.houses]
        if prop.houses == 0:
            prop.rent = prop.rents[0] * 2

    def reset(self, prop: Property):
        if prop.owner is None:
            raise Exception(prop.name + " can't be reset because it's owner is set to None")
        if isinstance(prop, Railroad):
            self.railroad_owners[prop.owner].remove(prop)
        elif isinstance(prop, Utility):
            self.utility_owners[prop.owner].remove(prop)
        prop.reset()
