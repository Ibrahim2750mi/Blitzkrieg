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
