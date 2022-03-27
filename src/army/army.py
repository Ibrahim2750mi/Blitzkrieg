import arcade

NAME = {1: "Swords Man", 2: "Bow Man", 3: "Cavalry", 4: "Pike Man", 5: "Cannons"}


class Unit(arcade.Sprite):
    def __init__(self, texture, center_x, center_y, index, enemy: bool = False):
        super(Unit, self).__init__(texture=texture, center_x=center_x, center_y=center_y)

        self.alive = 10
        self.injured = 0
        self.dead = 0

        self.health = 100

        self.enemy = enemy

        self._attack = None
        self.defence_percent = None

        self.index = index
        self.name = NAME.get(self.index + 1, "None")

        self.played = False

    def __str__(self):
        return f"\t{self.name}{['(enemy)' if self.enemy else ''][0]}:\n\nAlive: {self.alive}\nInjured: " \
               f"{self.injured}\nDead: {self.dead}\nHealth: {self.health}"

    def deduct_health(self, value, name=""):
        if name == "Pike Man" and self.name == "Cavalry":
            value += 15
        self.health -= (1 - self.defence_percent) * value
        if 10 * int(self.health / 10) + 1 != self.alive:
            self.injured = (100 - 10 * int(self.health / 10)) / 10
        self.alive = 10 - self.injured

        if self.injured > 1:
            self.injured -= 1
            self.dead += 1

    @property
    def attack(self):
        return self._attack * self.alive // 10

    @attack.setter
    def attack(self, val):
        self._attack = val


class Army:
    def __init__(self, kingdom):

        self.kingdom = kingdom

        self.morale = 100
        self.battles = 0
        self.battles_won = 0

        self.swords_man = 0
        self.bow_man = 0
        self.cavalry = 0
        self.pike_man = 0
        self.canons = 0

    @property
    def boost(self):
        ret = 0
        if self.kingdom.unhappiness == 0:
            ret += 5
        if self.kingdom.unemployed == 0:
            ret += 5
        if self.kingdom.hospital:
            ret += 5
        if self.kingdom.defence_office:
            ret += 15
        if self.morale > 80:
            ret += 3
        return ret

    def null(self):
        self.swords_man = 0
        self.bow_man = 0
        self.cavalry = 0
        self.pike_man = 0
        self.canons = 0

    def population_in_army(self):
        return 10 * (self.swords_man + self.bow_man + self.cavalry + self.pike_man + self.canons)
