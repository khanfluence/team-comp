from Hero import Hero


class Team:
    def __init__(self):
        self.heroes = list()
        self.stats = dict()

    def add_hero(self, hero: Hero) -> bool:
        if hero.name in self.heroes or len(self.heroes) == 5:
            return False

        self.heroes.append(hero.name)
        for hero_name, stat in hero.stats.items():
            self.stats[hero_name] = (self.stats[hero_name] + ((stat - self.stats[hero_name]) / len(self.heroes)))\
                if hero_name in self.stats else stat

        return True

    def rem_hero(self, hero: Hero):
        self.heroes.remove(hero.name)
        for hero_name, stat in hero.stats.items():
            self.stats[hero_name] = (self.stats[hero_name] * (len(self.heroes) + 1) - stat) / max(len(self.heroes), 1)

    def reset(self):
        self.heroes = list()
        self.stats = dict()
