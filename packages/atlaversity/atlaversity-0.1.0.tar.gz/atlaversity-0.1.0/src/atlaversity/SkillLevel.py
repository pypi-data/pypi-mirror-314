class SkillLevel:
    def __init__(self, name, days):
        self.name = name
        self.days = days
        self.set_level()

    def set_level(self):
        if self.days < 30:
            self.level = 0
        elif self.days < 90:
            self.level = 1
        elif self.days < 180:
            self.level = 2
        elif self.days < 300:
            self.level = 3
        elif self.days < 450:
            self.level = 4
        else:
            self.level = 5

    def __str__(self):
        s = f'{self.name} {self.level}({self.days})'
        return s
    
    def train(self, days):
        self.days += days
        self.set_level()
