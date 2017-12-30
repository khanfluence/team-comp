import os
import requests
from tkinter import *
from tkinter.ttk import *
from Hero import Hero
from SearchListbox import SearchListbox
from Team import Team


class Window(Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.root.title("teamcomp")
        self.grid()

        self.root.unbind_class("Listbox", "<space>")  # how to rebind action to Enter?
        self.root.bind("<Key>", lambda event: self.search(event))

        # hero list
        self.heroes = dict()
        self.hero_frm = Frame(self, borderwidth=0)
        self.hero_lst = SearchListbox(self.hero_frm, height=20)
        self.hero_scl = Scrollbar(self.hero_frm)
        self.init_hero_list()

        # team lists
        self.team1 = Team()
        self.team2 = Team()
        self.team_frm = Frame(self, borderwidth=0)
        self.team1_lst = SearchListbox(self.team_frm, height=5)
        self.team2_lst = SearchListbox(self.team_frm, height=5)
        self.init_team_lists()

        # add/remove buttons
        self.add_rem_frm = Frame(self, borderwidth=0)
        self.team1_add_btn = Button(self.add_rem_frm, text="-->", command=lambda: self.add_hero(self.team1,
                                                                                                self.team1_lst))
        self.team1_rem_btn = Button(self.add_rem_frm, text="<--", command=lambda: self.rem_hero(self.team1,
                                                                                                self.team1_lst))
        self.team2_add_btn = Button(self.add_rem_frm, text="-->", command=lambda: self.add_hero(self.team2,
                                                                                                self.team2_lst))
        self.team2_rem_btn = Button(self.add_rem_frm, text="<--", command=lambda: self.rem_hero(self.team2,
                                                                                                self.team2_lst))
        self.init_add_rem_buttons()

        # stats list
        self.stats_frm = Frame(self, borderwidth=0)
        self.stats_lbl = Label(self.stats_frm, text="Advantage")
        self.stats_lst = SearchListbox(self.stats_frm, height=20, width=26, font=("Consolas", "10"))
        self.stats_scl = Scrollbar(self.stats_frm)
        self.init_stats_list()

        # controls
        self.controls_lfrm = LabelFrame(self, text="Controls")
        self.show_rb_var = StringVar()
        self.show_team1_rb = Radiobutton(self.controls_lfrm, text="Radiant", variable=self.show_rb_var, value="team1")
        self.show_team2_rb = Radiobutton(self.controls_lfrm, text="Dire", variable=self.show_rb_var, value="team2")
        self.show_hero_rb = Radiobutton(self.controls_lfrm, text="Hero", variable=self.show_rb_var, value="hero")
        self.show_stats_btn = Button(self.controls_lfrm, text="Show", command=self.show_stats)
        self.reset_teams_btn = Button(self.controls_lfrm, text="Reset", command=self.reset_teams)
        self.wipe_stats_btn = Button(self.controls_lfrm, text="Wipe", command=self.wipe_stats)
        self.init_controls()

    def init_hero_list(self):
        if not os.path.exists("heroes"):
            os.makedirs("heroes")

        with open("hero_list.txt", 'r') as f:
            for idx, line in enumerate(f.readlines()):
                hero_stat = line.strip().split(sep=', ')
                self.heroes[hero_stat[0]] = Hero(hero_stat[0], hero_stat[1])
                self.hero_lst.append(hero_stat[0])

        self.hero_lst.config(yscrollcommand=self.hero_scl.set)
        self.hero_scl.config(command=self.hero_lst.yview)
        hero_lbl = Label(self.hero_frm, text="Hero List")

        self.hero_frm.grid(row=0, column=0, rowspan=2, sticky=NS)
        self.hero_lst.grid(row=1, column=0)
        self.hero_scl.grid(row=1, column=1, sticky=NS)
        hero_lbl.grid(row=0, column=0)

    def init_team_lists(self):
        team1_lbl = Label(self.team_frm, text="Radiant")
        team2_lbl = Label(self.team_frm, text="Dire")

        self.team_frm.grid(row=0, column=2, sticky=N)
        team1_lbl.grid(row=0, column=3)
        self.team1_lst.grid(row=1, column=3, rowspan=5)

        self.team_frm.grid_rowconfigure(6, minsize=20)
        team2_lbl.grid(row=7, column=3)
        self.team2_lst.grid(row=8, column=3, rowspan=5)

    def init_add_rem_buttons(self):
        self.add_rem_frm.grid(row=0, column=1, sticky=N)
        self.add_rem_frm.grid_rowconfigure(0, minsize=40)
        self.team1_add_btn.grid(row=1)
        self.team1_rem_btn.grid(row=2)
        self.team2_add_btn.grid(row=3)
        self.team2_rem_btn.grid(row=4)

    def init_stats_list(self):
        self.stats_lst.config(yscrollcommand=self.stats_scl.set)
        self.stats_scl.config(command=self.stats_lst.yview)

        self.stats_frm.grid(row=0, column=3, rowspan=2, sticky=NS)
        self.stats_lst.grid(row=1, column=0)
        self.stats_scl.grid(row=1, column=1, sticky=NS)
        self.stats_lbl.grid(row=0, column=0)

    def init_controls(self):
        self.controls_lfrm.grid_columnconfigure(0, weight=1)
        self.controls_lfrm.grid_columnconfigure(1, weight=1)
        self.controls_lfrm.grid_columnconfigure(2, weight=1)
        self.controls_lfrm.grid(row=1, column=1, columnspan=2, sticky=NSEW)
        self.show_team1_rb.grid(row=0, column=0)
        self.show_team2_rb.grid(row=0, column=1)
        self.show_hero_rb.grid(row=0, column=2)
        self.show_stats_btn.grid(row=1, column=0)
        self.reset_teams_btn.grid(row=1, column=1)
        self.wipe_stats_btn.grid(row=1, column=2)

        self.show_team1_rb.invoke()

    def reset_teams(self):
        self.team1.reset()
        self.team2.reset()
        self.team1_lst.delete(0, END)
        self.team2_lst.delete(0, END)

    def wipe_stats(self):
        for file in [f for f in os.listdir("heroes") if f.endswith(".txt")]:
            os.remove(f"heroes/{file}")

        for hero_name in self.team1.heroes + self.team2.heroes:
            self.heroes[hero_name].fetch_stats()

        self.stats_lst.delete(0, END)

    # currently unused
    def update_hero_list(self):
        page = requests.get("https://www.dotabuff.com/heroes", headers={"user-agent": "Mozilla/5.0"})
        heroes_file = open("hero_list.txt", 'w')

        for hero_stat in re.findall(r'<a href="/heroes/(.+?)">.+?<div class="name">(.+?)</div>', re.search(
                '<div class="hero-grid">[\s\S]+</div></footer></section>', page.text).group()):
            self.heroes[hero_stat[1]] = Hero(hero_stat[1], hero_stat[0])
            self.hero_lst.append(hero_stat[1])
            heroes_file.write(f"{hero_stat[1]}, {hero_stat[0]}\n")

        heroes_file.close()
        self.hero_lst.grid(row=1, column=0)

    def add_hero(self, team: Team, team_lst):
        hero: Hero = self.get_selected_hero()

        if hero is not None and team.add_hero(hero):
            team_lst.append(hero.name)

    def rem_hero(self, team, team_lst):
        idx = team_lst.curselection()
        if not idx:
            return

        team.rem_hero(self.heroes[team_lst.get(idx)])
        team_lst.delete(idx[0])

    def get_selected_hero(self) -> Hero:
        idx = self.hero_lst.curselection()
        hero: Hero = None

        if bool(idx):
            hero = self.heroes[self.hero_lst.get(idx)]
            if not hero.stats:
                hero.fetch_stats()

        return hero

    def show_stats(self):
        if self.show_rb_var.get() == "hero":
            hero: Hero = self.get_selected_hero()

            if hero is not None:
                self.update_stats_list(hero.stats)
        else:
            self.update_stats_list(eval(f"self.{self.show_rb_var.get()}").stats)

    def update_stats_list(self, stats: dict):
        self.stats_lst.delete(0, END)
        for hero, stat in sorted(stats.items(), key=lambda item: item[1]):
            self.stats_lst.append(f"{hero:20} {stat:+.2f}")

        self.stats_lst.grid(row=1, column=0)

    def search(self, event):
        if event.widget.winfo_class() != "Listbox":
            return

        if event.char.isalpha() or event.char == ' ':
            event.widget.search(event.char)
