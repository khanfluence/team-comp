import os
import pickle
import re
import requests
import tkinter
from tkinter import ttk
from Hero import Hero
from SearchListbox import SearchListbox
from Team import Team


class Window(ttk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.root.title("teamcomp")
        self.grid()

        self.root.unbind_class("Listbox", "<space>")  # how to rebind action to Enter?
        self.root.bind("<Key>", lambda event: self.search(event))

        # hero list
        self.heroes = dict()
        self.hero_frm = ttk.Frame(self, borderwidth=0)
        self.hero_lst = SearchListbox(self.hero_frm, height=20)
        self.hero_scl = ttk.Scrollbar(self.hero_frm)
        self.init_hero_list()

        # team lists
        self.team1 = Team()
        self.team2 = Team()
        self.team_frm = ttk.Frame(self, borderwidth=0)
        self.team1_lst = SearchListbox(self.team_frm, height=5)
        self.team2_lst = SearchListbox(self.team_frm, height=5)
        self.init_team_lists()

        # add/remove buttons
        self.add_rem_frm = ttk.Frame(self, borderwidth=0)
        self.team1_add_btn = ttk.Button(self.add_rem_frm, text="-->", command=lambda: self.add_hero(self.team1,
                                                                                                    self.team1_lst))
        self.team1_rem_btn = ttk.Button(self.add_rem_frm, text="<--", command=lambda: self.rem_hero(self.team1,
                                                                                                    self.team1_lst))
        self.team2_add_btn = ttk.Button(self.add_rem_frm, text="-->", command=lambda: self.add_hero(self.team2,
                                                                                                    self.team2_lst))
        self.team2_rem_btn = ttk.Button(self.add_rem_frm, text="<--", command=lambda: self.rem_hero(self.team2,
                                                                                                    self.team2_lst))
        self.init_add_rem_buttons()

        # stats list
        self.stats_frm = ttk.Frame(self, borderwidth=0)
        self.stats_lbl = ttk.Label(self.stats_frm, text="Counters")
        self.stats_lst = SearchListbox(self.stats_frm, height=20, width=26, font=("Consolas", "10"))
        self.stats_scl = ttk.Scrollbar(self.stats_frm)
        self.init_stats_list()

        # controls
        self.controls_lfrm = ttk.LabelFrame(self, text="Controls")
        self.show_rb_var = tkinter.StringVar()
        self.show_team1_rb = ttk.Radiobutton(self.controls_lfrm, text="Radiant", variable=self.show_rb_var,
                                             value="team1")
        self.show_team2_rb = ttk.Radiobutton(self.controls_lfrm, text="Dire", variable=self.show_rb_var, value="team2")
        self.show_hero_rb = ttk.Radiobutton(self.controls_lfrm, text="Hero", variable=self.show_rb_var, value="hero")
        self.show_stats_btn = ttk.Button(self.controls_lfrm, text="Show", command=self.show_stats)
        self.reset_teams_btn = ttk.Button(self.controls_lfrm, text="Clear", command=self.clear_teams)
        self.clear_stats_btn = ttk.Button(self.controls_lfrm, text="Wipe", command=self.wipe_stats)
        self.init_controls()

    def init_hero_list(self):
        if os.path.isfile("heroes.dat"):
            with open("heroes.dat", "rb") as f:
                self.heroes = pickle.load(f)
        else:
            self.init_heroes()

        for name in self.heroes.keys():
            self.hero_lst.append(name)

        self.hero_lst.config(yscrollcommand=self.hero_scl.set)
        self.hero_scl.config(command=self.hero_lst.yview)
        hero_lbl = ttk.Label(self.hero_frm, text="Heroes")

        self.hero_frm.grid(row=0, column=0, rowspan=2, sticky=tkinter.NS)
        self.hero_lst.grid(row=1, column=0)
        self.hero_scl.grid(row=1, column=1, sticky=tkinter.NS)
        hero_lbl.grid(row=0, column=0)

    def init_team_lists(self):
        team1_lbl = ttk.Label(self.team_frm, text="Radiant")
        team2_lbl = ttk.Label(self.team_frm, text="Dire")

        self.team_frm.grid(row=0, column=2, sticky=tkinter.N)
        team1_lbl.grid(row=0, column=3)
        self.team1_lst.grid(row=1, column=3, rowspan=5)

        self.team_frm.grid_rowconfigure(6, minsize=20)
        team2_lbl.grid(row=7, column=3)
        self.team2_lst.grid(row=8, column=3, rowspan=5)

    def init_add_rem_buttons(self):
        self.add_rem_frm.grid(row=0, column=1, sticky=tkinter.N)
        self.add_rem_frm.grid_rowconfigure(0, minsize=40)
        self.team1_add_btn.grid(row=1)
        self.team1_rem_btn.grid(row=2)
        self.team2_add_btn.grid(row=3)
        self.team2_rem_btn.grid(row=4)

    def init_stats_list(self):
        self.stats_lst.config(yscrollcommand=self.stats_scl.set)
        self.stats_scl.config(command=self.stats_lst.yview)

        self.stats_frm.grid(row=0, column=3, rowspan=2, sticky=tkinter.NS)
        self.stats_lst.grid(row=1, column=0)
        self.stats_scl.grid(row=1, column=1, sticky=tkinter.NS)
        self.stats_lbl.grid(row=0, column=0)

    def init_controls(self):
        self.controls_lfrm.grid_columnconfigure(0, weight=1)
        self.controls_lfrm.grid_columnconfigure(1, weight=1)
        self.controls_lfrm.grid_columnconfigure(2, weight=1)
        self.controls_lfrm.grid(row=1, column=1, columnspan=2, sticky=tkinter.NSEW)
        self.show_team1_rb.grid(row=0, column=0)
        self.show_team2_rb.grid(row=0, column=1)
        self.show_hero_rb.grid(row=0, column=2)
        self.show_stats_btn.grid(row=1, column=0)
        self.reset_teams_btn.grid(row=1, column=1)
        self.clear_stats_btn.grid(row=1, column=2)

        # team 1 selected by default
        self.show_team1_rb.invoke()

    def clear_teams(self):
        self.team1.reset()
        self.team2.reset()
        self.team1_lst.delete(0, tkinter.END)
        self.team2_lst.delete(0, tkinter.END)

    # wipe cached stats and fetch fresh stats for heroes on teams
    def wipe_stats(self):
        for hero in self.heroes.values():
            hero.stats = dict()

        for hero_name in self.team1.heroes + self.team2.heroes:
            self.heroes[hero_name].fetch_stats()

        self.stats_lst.delete(0, tkinter.END)

    # initialize hero dict and SearchListbox
    def init_heroes(self):
        page = requests.get("https://www.dotabuff.com/heroes", headers={"user-agent": "Mozilla/5.0"})
        self.hero_lst.delete(0, tkinter.END)
        self.heroes = dict()

        for hero_info in re.findall(r'<a href="/heroes/(.+?)">.+?<div class="name">(.+?)</div>', re.search(
                '<div class="hero-grid">[\s\S]+</div></footer></section>', page.text).group()):
            self.heroes[hero_info[1]] = Hero(hero_info[1], hero_info[0])
            self.hero_lst.append(hero_info[1])

    # unused, has no button; doable by deleting heroes.dat before run
    def refresh_heroes(self):
        self.init_heroes()
        self.wipe_stats()

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

        if bool(idx):  # or idx == 0?
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
        self.stats_lst.delete(0, tkinter.END)
        for hero, stat in sorted(stats.items(), key=lambda item: item[1], reverse=True):
            self.stats_lst.append(f"{hero:20} {stat:+.2f}")

        self.stats_lst.grid(row=1, column=0)

    # performed on window close
    def write_stats(self):
        with open("heroes.dat", 'wb') as f:
            pickle.dump(self.heroes, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def search(event):
        if event.widget.winfo_class() == "Listbox" and (event.char.isalpha() or event.char == ' '):
            event.widget.search(event.char)
