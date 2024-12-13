from Mage import *
from Turn import *

class Game:
    def __init__(self, cfg) -> None:
        self.config = cfg
        self.all_turns = []
        self.comments = []
        self.all_mages = []

    def save_to_file(self, file):
        f = open(file, 'w')
        row = 0
        comment = 0
        for i,m in enumerate(self.all_turns[0].start_mages):
            if i > 0:
                f.write(',')
            f.write(str(m.id))
        f.write('\n')
        row += 1
        for i,m in enumerate(self.all_turns[0].start_mages):
            if i == 0:
                f.write('#')
            else:
                f.write(',')
            f.write(m.name)
        f.write('\n')
        row += 1
        for i,m in enumerate(self.all_turns[0].start_mages):
            if i == 0:
                f.write('#')
            else:
                f.write(',')
            f.write(m.comment)
        f.write('\n')
        row += 1
        for t in self.all_turns:
            while len(self.comments) > comment and self.comments[comment][0] == row:
                f.write(self.comments[comment][1])
                f.write('\n')
                comment += 1
                row += 1
            for i,s in enumerate(t.study):
                if i > 0:
                    f.write(',')
                f.write(str(s))
            f.write('\n')
            row += 1
        while len(self.comments) > comment and self.comments[comment][0] == row:
            f.write(self.comments[comment][1])
            f.write('\n')
            comment += 1
            row += 1

    def read_plan_from_file(self, file, turn):
        f = open(self.config.data_dir + file, 'r')
        strs = f.read().splitlines()
        if len(strs[0].split(',')) != len(self.all_mages):
            raise ValueError('mages in plan file does not match the mage list')
        for i,mage_id in enumerate(strs[0].split(',')):
            if int(mage_id.strip()) != self.all_mages[i].id:
                raise ValueError('mages in plan file does not match the mage list')
        for i,comment in enumerate(strs[2][1:].split(',')):
            self.all_mages[i].comment = comment
        last_mages = self.all_mages
        turn_num = turn
        for i in range(3,len(strs)):
            if strs[i][0] != '#':
                p = Turn(last_mages, strs[i], turn_num)
                self.all_turns.append(p)
                last_mages = p.end_mages
                turn_num += 1
            else:
                self.comments.append((i, strs[i]))

    def add_new_turn(self):
        if len(self.all_turns) > 0:
            mages = self.all_turns[len(self.all_turns) - 1].end_mages
            turn_num = self.all_turns[len(self.all_turns) - 1].num + 1
        else:
            mages = self.all_mages
            turn_num = 1
        empty_study = ',' * (len(mages) - 1)
        turn = Turn(mages, empty_study, turn_num)
        self.all_turns.append(turn)

    # def find_by_id(self, mage_id):
    #     for m in self.all_mages:
    #         if m.id == int(mage_id):
    #             return m
    #     return None
    
    def find_num_by_id(self, mage_id) -> int:
        for i,m in enumerate(self.all_mages):
            if m.id == int(mage_id):
                return i
        return -1

    def read_mages_from_file(self, faction, turn):
        file = self.config.data_dir + 'mages' + str(faction).zfill(2) + str(turn).zfill(2) + '.csv'
        f = open(file, 'r')
        strs = f.read().splitlines()
        for i, mage in enumerate(strs[0].split(',')[1:]):
            d = mage.split(' ', 1)
            m = Mage(int(d[0]), d[1])
            for skill in strs[1:]:
                d = skill.split(',')
                d[0] = d[0].strip()
                if int(d[i + 1]) > 0 and d[0] != 'COMB' and d[0] != 'OBSE':
                    s = SkillLevel(d[0], int(d[i + 1]))
                    m.add_skill(s)
            self.all_mages.append(m)
