from date.date import Date
from .play import Play

import pandas as pd
import io
import requests
import json

from typing import Type

class Game():
    def __init__(self, game_pk: int):
        url = f"https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&game_pk={game_pk}"
        s = requests.get(url).content
        self._game_data = pd.read_csv(io.StringIO(s.decode('utf-8')))

        self._home: str = self._game_data.at[0, "home_team"]
        self._away: away = self._game_data.at[0, "away_team"]
        self._game_pk: int = game_pk
        self._date: Type["Date"] = Date.fromDateString(str(self._game_data.at[0, "game_date"]))

        self._home_score = self._game_data.loc[:, "home_score"].max()
        self._away_score = self._game_data.loc[:, "away_score"].max()

        self._home_lineup = self._game_data.loc[self._game_data.inning_topbot == "Top"].batter.unique()
        self._away_lineup = self._game_data.loc[self._game_data.inning_topbot != "Top"].batter.unique()

        self._home_score = self._game_data.loc[:, "post_home_score"].max()
        self._away_score = self._game_data.loc[:, "post_away_score"].max()

        # finds the url of the game based on the game_pk information stored in the at-bat data
        game_url = f"https://baseballsavant.mlb.com/gf?game_pk={self._game_pk}"
        game = requests.get(game_url)
    
        # load the given game's json file
        self._game_json = json.loads(game.text)
        self._away_json = self._game_json["team_away"]
        self._home_json = self._game_json["team_home"]
    
    def getHome(self):
        return self._home

    def getAway(self):
        return self._away

    def getHomeScore(self):
        return self._home_score

    def getAwayScore(self):
        return self._away_score

    def getHomeLineup(self):
        return self._home_lineup

    def getAwayLineup(self):
        return self._away_lineup

    def getGamePK(self):
        return self._game_pk

    def getDate(self):
        return self._date

    def getData(self):
        return self._game_data

    def getGameJSON(self):
        return self._game_json.copy()

    def getAwayJSON(self):
        return self._away_json

    def getHomeJSON(self):
        return self._home_json

    def getGameHighlights(self, plays=10, team=None):
        df = self._game_data.copy()

        if plays <= 0:
            raise ValueError("Plays must be greater than 0")

        if team.upper() not in [None, "HOME", "AWAY"]:
            raise ValueError("Team must be None, \"HOME\", or \"AWAY\"")

        # extra logic for when a home or away team is specified
        key = None if team else abs
        ascending = False if not team else (True, False)[team.lower() == "home"]

        # removes all non-events (balls, strikes, etc.)
        # then sorts for highest win expectancy for either team
        # then only keeps the top plays
        # also make sure the plays are in chronological order of the game
        df = df.loc[df.events.notnull()]
        df = df.sort_values(by="delta_home_win_exp", key=key, ascending=ascending)
        df = df.head(plays)
        df = df.sort_values(by="pitch_number", ascending=True)
        df = df.sort_values(by="at_bat_number", ascending=True)

        return [Play(self, row) for index, row in df.iterrows()]

    def getHomeTeamHighlights(self, plays=10):
        return self.getGameHighlights(plays, "home")

    def getAwayTeamHighlights(self, plays=10):
        return self.getGameHighlights(plays, "away")

    def __str__(self) -> str:
        return f"{self._away} - {self._home}, Final: {self._away_score}-{self._home_score}, Date: {self._date}, GamePK: {self._game_pk}"

