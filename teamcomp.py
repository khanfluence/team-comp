import re
import requests


def usage():
    print(f"{'HERO':15}add HERO to team\n"
          f"{'-HERO':15}remove HERO from team\n"
          f"{'best [n]':15}show [n] best matchups for team\n"
          f"{'worst [n]':15}show [n] worst matchups for team\n"
          f"{'HERO best [n]':15}show [n] best matchups for HERO\n"
          f"{'HERO worst [n]':15}show [n] worst matchups for HERO\n"
          f"{'wipe':15}clear team\n"
          f"{'team':15}show team\n"
          f"{'?':15}help\n"
          f"{'gg':15}exit\n",
          "=" * 20, sep='', end='\n\n')


def print_stats(cmd, stats):
    cmd = cmd.split()
    order = "best" if "best" in cmd else "worst"

    if cmd[0] != order:
        try:
            data = fetch_stats(cmd[0])
        except AttributeError:
            return
        stats = {data[i]: float(data[i + 1]) for i in range(0, len(data), 4)}

    heroes = sorted(stats.items(), key=lambda item: item[1], reverse=True if order == "best" else False)
    for hero in heroes[0:len(heroes) if len(cmd) - cmd.index(order) == 1 else int(cmd[-1])]:
        print(f"{hero[0]:20} {hero[1]:+.2f}")

    print("=" * 10, end='\n\n')


def print_team(team):
    print("Team: ", end='')
    print(*team, sep=', ', end='\n\n')


def sanitize(hero):
    return hero.replace(' ', '-').replace("'", "").lower()


def fetch_stats(hero):
    try:
        page = requests.get(f'https://www.dotabuff.com/heroes/{sanitize(hero)}/matchups?date=patch_7.06f',
                            headers={"user-agent": "Mozilla/5.0"})
    except AttributeError:
        print(f"Couldn't find {hero}.\n")
        raise

    return re.findall(r'<td (?:class=".+?".+?)?data-value="(.+?)">', re.search(
        r"<section><header>Most Successful Matchups[\s\S]+</section>", page.text).group())


def add(hero, stats, team):
    try:
        data = fetch_stats(hero)
    except AttributeError:
        return

    if hero not in team:
        team.append(hero)

        for i in range(0, len(data), 4):
            stats[data[i]] = (stats[data[i]] + ((float(data[i + 1]) - stats[data[i]]) / len(team)))\
                if data[i] in stats else float(data[i + 1])
    else:
        print(f"Already added {hero}.\n")
        return

    print_team(team)


def remove(hero, stats, team):
    try:
        data = fetch_stats(hero)
        team.remove(hero)

        for i in range(0, len(data), 4):
            stats[data[i]] = (stats[data[i]] * (len(team) + 1) - float(data[i + 1])) / max(len(team), 1)
    except (AttributeError, ValueError) as _:
        print(f"Couldn't find {hero}.\n")
        return

    print_team(team)


def main():
    stats = {}
    team = []
    usage()

    while True:
        cmd = input().lower()

        if cmd == "gg":
            break
        elif cmd == "?":
            usage()
        elif cmd == "team":
            print_team(team)
        elif cmd == "wipe":
            stats = {}
            team = []
            print("Done.\n")
        elif "best" in cmd or "worst" in cmd:
            print_stats(cmd, stats)
        elif cmd[0] == '-':
            remove(cmd[1:].title(), stats, team)
        else:
            add(cmd.title(), stats, team)


if __name__ == "__main__":
    main()
