import arcade

NAME = {1: "Swords Man", 2: "Bow Man", 3: "Cavalry", 4: "Pike Man", 5: "Cannons"}


class Unit(arcade.Sprite):
    def __init__(self, texture, center_x, center_y, index, enemy: bool = False):
        super(Unit, self).__init__(texture=texture, center_x=center_x, center_y=center_y)

        self.population = 10
        self.injured = 0
        self.dead = 0

        self.health = 100

        self.enemy = enemy

        self.attack = None
        self.defence_percent = None

        self.index = index
        self._name = NAME[self.index + 1]

    def __str__(self):
        return f"\t{self._name}{['(enemy)' if self.enemy else ''][0]}:\n\nAlive: {self.population}\nInjured: " \
               f"{self.injured}\nDead: {self.dead}"


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
