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
        self.game_data: pd.DataFrame = pd.read_csv(io.StringIO(s.decode('utf-8')))

        self.home: str = self.game_data.at[0, "home_team"]
        self.away: str = self.game_data.at[0, "away_team"]
        self.game_pk: int = game_pk
        self.date: Type["Date"] = Date.fromDateString(str(self.game_data.at[0, "game_date"]))

        # self.home_score: int = self.game_data.loc[:, "home_score"].max()
        # self.away_score: int = self.game_data.loc[:, "away_score"].max()

        self.home_lineup = self.game_data.loc[self.game_data.inning_topbot == "Top"].batter.unique()
        self.away_lineup = self.game_data.loc[self.game_data.inning_topbot != "Top"].batter.unique()

        self.home_score: int = self.game_data.loc[:, "post_home_score"].max()
        self.away_score: int = self.game_data.loc[:, "post_away_score"].max()

        # finds the url of the game based on the game_pk information stored in the at-bat data
        game_url = f"https://baseballsavant.mlb.com/gf?game_pk={self.game_pk}"
        game = requests.get(game_url)
    
        # load the given game's json file
        self.game_json = json.loads(game.text)
        self.away_json = self.game_json["team_away"]
        self.home_json = self.game_json["team_home"]
    
    def getHome(self) -> str:
        return self.home

    def getAway(self) -> str:
        return self.away

    def getHomeScore(self) -> int:
        return self.home_score

    def getAwayScore(self) -> int:
        return self.away_score

    def getHomeLineup(self):
        return self.home_lineup

    def getAwayLineup(self):
        return self.away_lineup

    def getGamePK(self) -> int:
        return self.game_pk

    def getDate(self) -> Type["Date"]:
        return self.date

    def getData(self) -> pd.DataFrame:
        return self.game_data

    def getGameJSON(self):
        return self.game_json.copy()

    def getAwayJSON(self):
        return self.away_json

    def getHomeJSON(self):
        return self.home_json

    def getGameHighlights(self, plays=10, team=None):
        df = self.game_data.copy()

        if plays <= 0:
            raise ValueError("Plays must be greater than 0")

        if team is not None and team.upper() not in ["HOME", "AWAY"]:
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
        return f"{self.away} - {self.home}, Final: {self.away_score}-{self.home_score}, Date: {self.date}, GamePK: {self.game_pk}"

