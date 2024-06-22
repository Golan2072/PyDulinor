#PyDulinor - MegaTraveller Hard Times Subsector Collapse Script
#By Omer Golan-Joel, June 19th, 2024
#Open Source Code
#Traveller is copyrighted (c) by Marc Miller and Far Future Enterprises. This script is posted under their Fair Use policy.

import random

degrees ={0: 0, 1: 0, 2: 0, 3:0, 4:0, 5:-1, 6:-1, 7:-2, 8:-2, 9:-3, 10:-3, 11:-4, 12:-4, 13:-5, 14:-5, 15:-6, 16:-6, 17:-7, 18:-7, 19:-8, 20:-8, 21:-9, 22:-9, 23:-10, 24:-10, 25:-11, 26:-11, 17:-12, 28:-12, 29:-13, 30:-13}


def change (roll):
    if roll <=0:
        roll = 0
    elif roll > 30:
        roll = 30
    return degrees[roll]

def dice(n, sides):
    die = 0
    roll = 0
    while die < n:
        roll = roll + random.randint(1, sides)
        die += 1
    return roll


def list_stringer(input_list):
    output_list = []
    for item in input_list:
        output_list.append(str(item))
    return ' '.join(output_list)


def pseudo_hex(num):
    num = int(num)
    code = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F", "G", "X", "J", "K", "L", "M", "N", "P", "Q",
            "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    num = code[num]
    return num


def hex_to_int(num):
    code = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15, "G":16, "X": 17}
    return int(code[num])

def uwp_parser (uwp):
    uwp_list = []
    for digit in uwp:
        if digit == "-":
            pass
        else:
            uwp_list.append(int(hex_to_int(digit)))
    return uwp_list


class World:
    def __init__(self, uwp_string, pop_multiplier, warzone, zone):
        self.uwp = uwp_string
        self.multiplier = pop_multiplier
        self.warzone = warzone
        self.zone = zone
        self.uwp_list = uwp_parser(self.uwp)
        self.biodamage = False
        self.tl_lost = 0
        self.multiplier_lost = 0
        self.events = []
        self.xenophobic = False
        self.xenophobia_level = 0
        self.isolationism = False
        self.starport_destruction = 0
        self.failing = False
        self.doomed = False
        output_uwp_string = ""
        self.biosphere()
        self.starport_damage()
        self.tech_collapse()
        self.xenophobia()
        self.isolationism_check()
        self.pop_decline()
        self.gov_change()
        self.uwp_stringer()

    def biosphere(self):
        roll = dice(2, 6)
        if self.warzone == "War":
            roll +=1
        elif self.warzone == "Intense":
            roll +=2
        elif self.warzone == "Black":
            roll +=3
        if self.uwp_list[0] == 10:
            roll += 1
        if self.uwp_list[4] in (9, 10):
            roll +=1
        if roll >=14:
            self.biodamage = True
            self.uwp_list[0] = 0
            self.events.append("Starport destroyed!")
            second_roll = dice(2, 6)
            if self.warzone == "Black":
                second_roll += 2
            if second_roll <= 3:
                self.events.append("Biosphere damage: mild temporary temperature decrease")
            elif second_roll in (4, 5):
                self.events.append("Biosphere damage: permanent temperature decrease")
            elif second_roll in (6, 7, 8):
                self.events.append("Biosphere damage: atmosphere tained")
                if self.uwp_list[2] == 5:
                    self.uwp_list[2] = 4
                elif self.uwp_list[2] == 6:
                    self.uwp_list[2] = 7
                elif self.uwp_list[2] == 8:
                    self.uwp_list[2] = 9
            elif second_roll in (9, 10):
                self.events.append("Biosphere damage: atmosphere tained")
                if self.uwp_list[2] == 5:
                    self.uwp_list[2] = 4
                elif self.uwp_list[2] == 6:
                    self.uwp_list[2] = 7
                elif self.uwp_list[2] == 8:
                    self.uwp_list[2] = 9
                self.uwp_list[4] -= 1
                if self.uwp_list[4] < 0:
                    self.uwp_list[4] = 0
                self.uwp_list[7] -= 3
                if self.uwp_list[7] <0:
                   self.uwp_list[7] = 0
            elif second_roll in (11, 12):
                self.events.append("Biosphere damage: severe destruction")
                self.uwp_list[2] = 12
                self.uwp_list[4] -= 2
                if self.uwp_list[4] < 0:
                    self.uwp_list[4] = 0
                self.uwp_list[7] -= 6
                if self.uwp_list[7] <0:
                   self.uwp_list[7] = 0
            elif second_roll >= 13:
                self.events.append("Biosphere damage: annihilation!")
                self.uwp_list[2] = 12
                self.uwp_list[4] = 0
                self.uwp_list[5] = 0
                self.uwp_list[6] = 0
                self.uwp_list[7] = 0
            else:
                pass
        else:
            self.biodamage = False
            pass
    
    def starport_damage(self):
        zone_table = {"Safe": {0:0, 10:0, 11:0, 12: 0, 13:0}, "Frontier": {0:0, 10:2, 11:0, 12: 0, 13:0}, "Outlands": {0:0, 10:3, 11: 2, 12:1, 13:0}, "Wilds": {0:0, 10:3, 11:3, 12: 2, 13: 1}}
        warzone_table = {"Normal": {0:0, 10:0, 11:0, 12: 0, 13:0}, "War": {0:0, 10:1, 11:1, 12: 1, 13:0}, "Intense": {0:0, 10:2, 11: 2, 12:1, 13:0}, "Black": {0:0, 10:3, 11:2, 12: 2, 13: 1}}
        pop_table= {0: {0:0, 10:2, 11:2, 12: 1, 13:0}, 1: {0:0, 10:2, 11:2, 12: 1, 13:0}, 2: {0:0, 10:2, 11:2, 12: 1, 13:0}, 3: {0:0, 10:1, 11:1, 12: 0, 13:0}, 4: {0:0, 10:1, 11:1, 12: 0, 13:0}}
        tech_table = {0: {0:0, 10:8, 11:7, 12: 5, 13:3}, 1: {0:0, 10:8, 11:7, 12: 5, 13:3}, 2: {0:0, 10:8, 11:7, 12: 5, 13:3}, 3: {0:0, 10:8, 11:7, 12: 5, 13:3}, 4: {0:0, 10:8, 11:7, 12: 5, 13:3}, 5: {0:0, 10:5, 11:4, 12: 3, 13:1}, 6: {0:0, 10:5, 11:4, 12: 3, 13:1}, 7: {0:0, 10:3, 11:1, 12: 0, 13:0}, 8: {0:0, 10:3, 11:1, 12: 0, 13:0}, 9: {0:0, 10:1, 11:0, 12: 0, 13:0}, 10: {0:0, 10:1, 11:0, 12: 0, 13:0}}
        roll = dice(1, 6)
        roll += zone_table[self.zone][self.uwp_list[0]]
        roll += warzone_table[self.warzone][self.uwp_list[0]]
        if self.uwp_list[4] in range (0, 5):
            roll += pop_table[self.uwp_list[4]][self.uwp_list[0]]
        else:
            pass
        if self.uwp_list[7] in range (0, 11):
            roll += tech_table[self.uwp_list[7]][self.uwp_list[0]]
        else:
            pass
        if roll >= 5:
            self.events.append("Starport damaged")
            self.starport_destruction = change(roll)
            self.uwp_list[0] -= change(roll)
            if self.uwp_list[0] >= 17:
                self.uwp_list[0] = 17
        if roll in range (5, 8) and self.zone != "Wilds":
            if dice(2, 6)  >= 7:
              self.events.append("Bases destroyed")
            else:
                pass
        elif roll >= 8:
            self.events.append("Bases destroyed")
        
    def tech_collapse(self):
        roll = dice (1,6)
        starport_table = {11:1, 12:2, 13:3, 14:4, 0:5}
        tl_table = {1:-10, 2:-8, 3:-6, 4:-4, 5:-4, 6:-2, 7:-2, 8:0, 9:0, 10:1, 11:1, 12:3, 13:3, 14:5, 15:7, 16:7}
        if self.uwp_list[0] in (11, 12, 13, 14, 0):
            roll += starport_table[self.uwp_list[0]]
        else:
            pass
        if self.uwp_list[2] in range (0,4) or self.uwp_list[2] in (10, 11):
            roll += 1
        elif self.uwp_list[2] == 12:
            roll +=2
        else:
            pass
        if self.uwp_list[3] in [0, 1, 10]:
            roll += 1
        else:
            pass
        if self.uwp_list[3] > 0 and self.uwp_list[2] > 10:
            roll += 1
        else:
            pass
        if self.uwp_list[4] in range (0, 5):
            roll += 4
        elif self.uwp_list[4] == 5:
            roll += 2
        elif self.uwp_list[4] == 6:
            roll += 1
        else:
            pass
        if self.uwp_list[5] in (5, 6):
            roll -= 1
        elif self.uwp_list[5] in (0, 2, 3, 7, 11, 12, 13, 14, 15):
            roll += 1
        roll += tl_table[self.uwp_list[7]]
        if self.zone == "Outland":
            roll += 1
        elif self.zone == "Wilds":
            roll += 3
        if roll <= 4:
            self.events.append("Technology preserved")
            pass
        else:
            self.uwp_list[7] += change(roll)
            if self.uwp_list[7] < 0:
                self.uwp_list[7] = 0
            self.tl_lost = -change(roll)
    
    def xenophobia(self):
        roll = dice(1, 3)
        fluids = False
        if self.uwp_list[2] >= 10 and self.uwp_list[3] > 0:
            fluids = True
        else:
            pass
        if self.biodamage == True:
            roll += 6
        if self.uwp_list[2] in (0, 1):
            roll += 1
        if self.uwp_list[3] in (0, 1) or fluids == True:
            roll += 1
        if self.uwp_list[4] in (0, 1, 2):
            roll -= 1
        elif self.uwp_list[4] in (6, 7, 8):
            roll += 1
        elif self.uwp_list[4] in (9, 10):
            roll += 2
        else:
            pass
        if self.uwp_list[5] >= 10:
            roll += 1
        if self.zone == "Outland":
            roll += 1
        if self.zone == "Wilds":
            roll += 2
        roll += self.starport_destruction
        self.xenophobia_level = -change(roll)
    
    def isolationism_check(self):
        if self.xenophobia_level >= 1:
            roll = dice(2, 6)
            if self.uwp_list[2] in (5, 6, 8):
                roll += 1
            if self.uwp_list[2] < 10 and self.uwp_list[3] > 0:
                roll +=1
            if self.uwp_list[7] <= 4:
                roll += 7
            elif self.uwp_list[7] == 5:
                roll += 3
            elif self.uwp_list[7] == 6:
                roll += 2
            elif self.uwp_list[7] == 7:
                roll += 1
            else:
                pass
            if self.uwp_list[0] == 10:
                roll -= 5
            elif self.uwp_list[0] == 11:
                roll -= 4
            elif self.uwp_list[0] == 12:
                roll -= 2
            elif self.uwp_list[0] == 13:
                roll -= 1
            if roll >= 11:
                self.isolationism = True
            else:
                pass
        else:
            pass
    
    def pop_decline(self):
        roll = dice(1, 3)
        environmental_modifier = 0
        other_modifier = 0
        atmosphere_table = {0: {12: 5, 0: 5, 1: 5, 10: 5, 11: 5, 2: 5, 3: 5, 4: 3, 7: 3, 9: 3}, 1: {12: 5, 0: 5, 1: 5, 10: 5, 11: 5, 2: 5, 3: 5, 4: 3, 7: 3, 9: 3}, 2: {12: 5, 0: 5, 1: 5, 10: 5, 11: 5, 2: 5, 3: 5, 4: 3, 7: 3, 9: 3}, 3: {12: 5, 0: 5, 1: 5, 10: 5, 11: 5, 2: 4, 3: 3, 4: 2, 7: 2, 9: 2}, 4: {12: 4, 0: 2, 1: 2, 10: 2, 11: 2, 2: 2, 3: 2, 4: 1, 7: 1, 9: 1}, 5: {12: 2, 0: 1, 1: 1, 10: 1, 11: 1, 2: 1, 3: 1, 4: 0, 7: 0, 9: 0}, 6: {12: 2, 0: 1, 1: 1, 10: 1, 11: 1, 2: 1, 3: 1, 4: 0, 7: 0, 9: 0}, 7: {12: 1, 0: 0, 1: 0, 10: 0, 11: 0, 2: 0, 3: 0, 4: 0, 7: 0, 9: 0}, 8: {12: 1, 0: 0, 1: 0, 10: 0, 11: 0, 2: 0, 3: 0, 4: 0, 7: 0, 9: 0}}
        hydrographics_table = {0: {0: 5, 1: 3, 2: 2, 10: 2}, 1: {0: 5, 1: 3, 2: 2, 10: 2}, 2: {0: 5, 1: 3, 2: 2, 10: 2}, 3: {0: 4, 1: 2, 2: 1, 10: 1}, 4: {0: 2, 1: 1, 2: 0, 10: 0}, 5: {0: 1, 1: 0, 2: 0, 10: 0}, 6: {0: 1, 1: 0, 2: 0, 10: 0}, 7: {0: 0, 1: 0, 2: 0, 10: 0}, 8: {0: 0, 1: 0, 2: 0, 10: 0}}
        population_table = {0: {"Normal": 0, "War": 0, "Intense": 1, "Black": 1}, 1: {"Normal": 0, "War": 0, "Intense": 1, "Black": 1}, 2: {"Normal": 0, "War": 0, "Intense": 1, "Black": 1}, 3: {"Normal": 0, "War": 1, "Intense": 2, "Black": 3}, 4: {"Normal": 0, "War": 1, "Intense": 2, "Black": 3}, 5: {"Normal": 0, "War": 1, "Intense": 2, "Black": 3}, 6: {"Normal": 0, "War": 2, "Intense": 3, "Black": 5}, 7: {"Normal": 0, "War": 2, "Intense": 3, "Black": 5}, 8: {"Normal": 0, "War": 2, "Intense": 3, "Black": 5}, 9: {"Normal": 0, "War": 1, "Intense": 2, "Black": 3}, 10: {"Normal": 0, "War": 1, "Intense": 2, "Black": 3}}
        if self.uwp_list[2] in (12, 0, 1, 11, 12, 3, 4, 7, 9):
            environmental_modifier += atmosphere_table[self.uwp_list[2]][self.uwp_list[7]]
        else:
            pass
        if self.uwp_list[2] in (0, 1, 2, 10):
            environmental_modifier += hydrographics_table[self.uwp_list[7]][self.uwp_list[3]]
        else:
            pass
        if environmental_modifier in (2, 3, 4):
            self.failing = True
        elif environmental_modifier >= 5:
            self.doomed = True
        else:
            pass
        if self.uwp_list[4] in range (0, 11):
             other_modifier += population_table[self.uwp_list[4]][self.warzone]
        else:
            pass
        if self.uwp_list[4] in (0, 1, 2):
            other_modifier -= 3
        elif self.uwp_list[4] in (3, 4, 5):
            other_modifier -= 2
        elif self.uwp_list[4] in (9, 10):
            other_modifier += 1
        else:
            pass
        roll += environmental_modifier + other_modifier
        if self.doomed == True:
            self.multiplier += change(roll)
            self.multiplier_lost = -change(roll)
            if self.multiplier <= 0:
                self.uwp_list[4] -= 1
            if self.uwp_list[4] < 0:
                self.uwp_list[4] = 0
        else:
            pass

    def gov_change(self):
        roll = dice (1, 6)
        if self.failing == True or self.doomed == True:
            roll += self.tl_lost - 2
            roll += self.multiplier_lost -1
            if roll < 0:
                roll = 0
            gov_table = {0: 1, 1: 8, 2: 2, 3: 9, 4: 3, 5: 7, 6: 8, 7: 4, 8: 5, 9: 5, 10: 11, 11: 12, 12: 10, 13: 12, 14: 14, 15:14}
            reverse_gov_table = {0: 0, 1: 2, 3: 4, 4: 7, 5: 8, 6: 9, 7: 5, 8: 6, 9: 3, 10: 12, 11: 10, 12: 11, 13: 14}
            gov_row = gov_table[self.uwp_list[5]]
            gov_row -= change(roll)
            if gov_row < 0:
                gov_row = 0
            else:
                pass
            new_gov = reverse_gov_table[gov_row]
            if new_gov < 0:
                new_gov = 0
            if new_gov > 15:
                new_gov = 0
            if new_gov != self.uwp_list[5]:
                self.uwp_list[5] = new_gov
                self.events.append("Revolution!")
                self.uwp_list[6] = dice(2, 6) - 7 + self.uwp_list[5]
                if self.uwp_list[6] < 0:
                    self.uwp_list[6] = 0
        else:
            pass
    
    def uwp_stringer(self):
        new_uwp_list = []
        for item in self.uwp_list:
            new_uwp_list.append(pseudo_hex(item))
        self.output_uwp_string = f"{new_uwp_list[0]}{new_uwp_list[1]}{new_uwp_list[2]}{new_uwp_list[3]}{new_uwp_list[4]}{new_uwp_list[5]}{new_uwp_list[6]}-{new_uwp_list[7]}"
                

if __name__ == "__main__":
    uwp = input("Please enter the world's UWP: ")
    zone = input("Please enter the world's Zone (Safe, Frontier, Wilds, Outland): ")
    warzone = input("Please enter the world's Warzone (Normal, War, Intense, Black): ")
    multiplier = int(input("Please enter teh world's population multiplier: "))
    planet = World(uwp_string=uwp, pop_multiplier=multiplier, warzone=warzone, zone=zone)
    print(f"New UWP: {planet.output_uwp_string} Pop Multipler: {planet.multiplier}, Xenophobia: {planet.xenophobia_level}, Isolationism: {planet.isolationism}, Events: {list_stringer(planet.events)}")
