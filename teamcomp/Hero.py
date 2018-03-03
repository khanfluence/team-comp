import re
import requests


class Hero:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.stats = dict()

    def fetch_stats(self):
        page = requests.get(f'https://www.dotabuff.com/heroes/{self.url}/counters',
                            headers={"user-agent": "Mozilla/5.0"})
        data = re.findall(r'<td (?:class=".+?".+?)?data-value="(.+?)">', re.search(
                r"<section><header>Matchups[\s\S]+</section>", page.text).group())

        for i in range(0, len(data), 4):
            self.stats[data[i]] = float(data[i + 1])
