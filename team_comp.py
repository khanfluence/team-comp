import re
import requests


def print_stats(cmd, stats):
    cmd = cmd.split()
    heroes = sorted(stats.items(), key=lambda item: item[1], reverse=True if cmd[0] == "best" else False)

    for hero in heroes[0:len(heroes) if len(cmd) == 1 else int(cmd[1]) + 1]:
        print(f"{hero[0]:20} {hero[1]:+.2f}")


def fetch_stats(cmd):
    page = requests.get(f"https://www.dotabuff.com/heroes/{cmd.replace(' ', '-')}/matchups?date=patch_7.06f",
                        headers={"user-agent": "Mozilla/5.0"})

    return re.findall(r'<td (?:class=".+?".+?)?data-value="(.+?)">', re.search(
        r"<section><header>Most Successful Matchups[\s\S]+</section>", page.text).group())


def add(cmd, stats, team):
    try:
        data = fetch_stats(cmd)
    except AttributeError:
        print(f"Couldn't find {cmd}.")
        return

    if cmd not in team:
        team.append(cmd.title())

        for i in range(0, len(data), 4):
            stats[data[i]] = (stats[data[i]] + ((float(data[i + 1]) - stats[data[i]]) / len(team)))\
                if data[i] in stats else float(data[i + 1])
    else:
        print(f"Already added {cmd}.")
        return

    print("Done.")


def remove(cmd, stats, team):
    try:
        data = fetch_stats(cmd)
        team.remove(cmd)

        for i in range(0, len(data), 4):
            stats[data[i]] = (stats[data[i]] * (len(team) + 1) - float(data[i + 1])) / max(len(team), 1)
    except (AttributeError, ValueError) as _:
        print(f"Couldn't find {cmd}.")
        return

    print("Done.")


def main():
    stats = {}
    team = []

    while True:
        cmd = input().lower()

        if cmd == "gg":
            break
        elif cmd == "team":
            print(*team, sep=',')
        elif "best" in cmd or "worst" in cmd:
            print_stats(cmd, stats)
        elif cmd[0] == '-':
            remove(cmd[1:], stats, team)
        else:
            add(cmd, stats, team)


if __name__ == "__main__":
    main()
