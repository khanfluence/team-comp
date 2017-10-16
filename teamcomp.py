import re
import requests


def usage():
    print(f"{'hero':10}add hero to team\n"
          f"{'-hero':10}remove hero from team\n"
          f"{'best [n]':10}show [n] best matchups for team\n"
          f"{'worst [n]':10}show [n] worst matchups for team\n"
          f"{'wipe':10}clear team\n"
          f"{'team':10}show team\n"
          f"{'?':10}help\n"
          f"{'gg':10}exit\n",
          "=" * 20, sep='', end='\n\n')


def print_stats(cmd, stats):
    cmd = cmd.split()
    heroes = sorted(stats.items(), key=lambda item: item[1], reverse=True if cmd[0] == "best" else False)

    for hero in heroes[0:len(heroes) if len(cmd) == 1 else int(cmd[1]) + 1]:
        print(f"{hero[0]:20} {hero[1]:+.2f}")

    print("=" * 10, end='\n\n')


def print_team(team):
    print("Team: ", end='')
    print(*team, sep=', ', end='\n\n')


def fetch_stats(cmd):
    page = requests.get(f"https://www.dotabuff.com/heroes/{cmd.replace(' ', '-')}/matchups?date=patch_7.06f",
                        headers={"user-agent": "Mozilla/5.0"})

    return re.findall(r'<td (?:class=".+?".+?)?data-value="(.+?)">', re.search(
        r"<section><header>Most Successful Matchups[\s\S]+</section>", page.text).group())


def add(cmd, stats, team):
    try:
        data = fetch_stats(cmd)
    except AttributeError:
        print(f"Couldn't find {cmd}.\n")
        return

    if cmd not in team:
        team.append(cmd.title())

        for i in range(0, len(data), 4):
            stats[data[i]] = (stats[data[i]] + ((float(data[i + 1]) - stats[data[i]]) / len(team)))\
                if data[i] in stats else float(data[i + 1])
    else:
        print(f"Already added {cmd}.\n")
        return

    print_team(team)


def remove(cmd, stats, team):
    try:
        data = fetch_stats(cmd)
        team.remove(cmd.title())

        for i in range(0, len(data), 4):
            stats[data[i]] = (stats[data[i]] * (len(team) + 1) - float(data[i + 1])) / max(len(team), 1)
    except (AttributeError, ValueError) as _:
        print(f"Couldn't find {cmd}.\n")
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
            remove(cmd[1:], stats, team)
        else:
            add(cmd, stats, team)


if __name__ == "__main__":
    main()
