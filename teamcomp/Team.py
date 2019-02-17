from collections import defaultdict
from Hero import Hero


class Team:
    def __init__(self):
        self.heroes = list()
        self.stats = defaultdict(float)

    def add_hero(self, hero: Hero) -> bool:
        if hero in self.heroes or len(self.heroes) == 5:
            return False

        self.heroes.append(hero)
        for hero in self.heroes:
            self.stats.pop(hero.name, None)
        self.calc_stats()
        return True

    def remove_hero(self, hero: Hero):
        self.heroes.remove(hero)
        if len(self.heroes) == 0:
            self.reset()
        else:
            self.calc_stats()

    def calc_stats(self):  # inefficient, but more correct than running averages
        self.stats = defaultdict(float)
        for hero_name in self.heroes[0].stats:
            if hero_name not in [hero.name for hero in self.heroes]:
                for hero in self.heroes:
                    self.stats[hero_name] += hero.stats[hero_name]
                self.stats[hero_name] /= len(self.heroes)

    def reset(self):
        self.heroes = list()
        self.stats = defaultdict(float)
