import os
import re
import requests


class Hero:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.stats = dict()

        if os.path.exists(f"heroes/{self.url}.txt"):
            self.read_stats()

    def read_stats(self):
        with open(f"heroes/{self.url}.txt", 'r') as f:
            for line in f.readlines():
                stat = line.strip().split(sep=', ')
                self.stats[stat[0]] = float(stat[1])

    def fetch_stats(self):
        page = requests.get(f'https://www.dotabuff.com/heroes/{self.url}/matchups',
                            headers={"user-agent": "Mozilla/5.0"})
        data = re.findall(r'<td (?:class=".+?".+?)?data-value="(.+?)">', re.search(
                r"<section><header>Most Successful Matchups[\s\S]+</section>", page.text).group())
        hero_file = open(f"heroes/{self.url}.txt", 'w')

        for i in range(0, len(data), 4):
            self.stats[data[i]] = float(data[i + 1])
            hero_file.write(f"{data[i]}, {data[i + 1]}\n")

        hero_file.close()
