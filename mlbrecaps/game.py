import pandas as pd
import io
import requests
import json

from functools import lru_cache, singledispatchmethod
from typing import List, Optional

from .team import Team
from .date import Date
from .player import Player
from .play import Play
from .utils import async_run, dataframe_from_url

class Game():

    @lru_cache(maxsize=3)
    def __new__(cls, game_pk: int):
        return super().__new__(cls)

    def __init__(self, game_pk: int):
        self._game_pk: int  = game_pk
        self._game_data: pd.DataFrame | None = None

        # finds the url of the game based on the game_pk information stored in the at-bat data
        game_url = f"https://baseballsavant.mlb.com/gf?game_pk={self._game_pk}"
        game = requests.get(game_url)

        # load the given game's json file
        self._game_json = json.loads(game.text)
        self._away_json = self._game_json["team_away"]
        self._home_json = self._game_json["team_home"]

        # Get home/away and date
        self._home: Team = Team(self._game_json["home_team_data"]["abbreviation"])
        self._away: Team = Team(self._game_json["away_team_data"]["abbreviation"])
        self._date: Date = Date(self._game_json["gameDate"])

        # Get both lineups
        self._home_lineup: List[int] = self._game_json["home_lineup"]
        self._away_lineup: List[int] = self._game_json["away_lineup"]

        # Get the final scores
        self._home_score: int = self._game_json["scoreboard"]["linescore"]["teams"]["home"]["runs"]
        self._away_score: int = self._game_json["scoreboard"]["linescore"]["teams"]["away"]["runs"]
    
    @singledispatchmethod
    def road_status(self, team: Team) -> str:
        raise ValueError("team must be of type Team")

    @road_status.register(Team)
    def _(self, team: Team) -> str:
        if self._away == team:
            return "AWAY"

        return "HOME"

    @property
    def home(self) -> Team:
        return self._home

    @property
    def away(self) -> Team:
        return self._away

    @property
    def home_score(self) -> int:
        return self._home_score

    @property
    def away_score(self) -> int:
        return self._away_score

    @property
    def home_lineup(self) -> List[int]:
        return self._home_lineup.copy()

    @property
    def away_lineup(self) -> List[int]:
        return self._away_lineup.copy()

    def get_lineup(self, team) -> List[int]:
        if team == self._away:
            return self.away_lineup()
            
        return self.home_lineup

    @property
    def game_pk(self) -> int:
        return self._game_pk

    @property
    def date(self) -> Date:
        return self._date.copy()

    @dataframe_from_url
    def __get_data(self) -> pd.DataFrame:
        return f"https://baseballsavant.mlb.com/statcast_search/csv?all=true&type=details&game_pk={self._game_pk}"

    @property
    def data(self) -> pd.DataFrame:
        return self.__get_data().copy()

    @property
    def game_json(self):
        return self._game_json.copy()

    @property
    def away_json(self):
        return self._away_json.copy()

    @property
    def home_json(self):
        return self._home_json.copy()

    def get_highlights(self, plays:int =10, team: Optional[str]=None):
        df = self.__get_data()

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
        df = df[df.events.notnull()]
        df = df.sort_values(by="delta_home_win_exp", key=key, ascending=ascending)
        df = df.head(plays)
        df = df.sort_values(by="pitch_number", ascending=True)
        df = df.sort_values(by="at_bat_number", ascending=True)

        rows = [row for index, row in df.iterrows()]
        return async_run(Play, self, rows)

    def get_home_highlights(self, plays=10):
        return self.get_highlights(plays, "home")

    def get_away_highlights(self, plays=10):
        return self.get_highlights(plays, "away")

    def get_player_highlights(self, player: Player, plays: int):
        df = self.__get_data()

        is_home_player = player.player_id in self.home_lineup

        df = df[df.events.notnull() & ((df.batter == player.player_id) | (df.pitcher == player.player_id))]
        df = df.sort_values(by="delta_home_win_exp", key=None, ascending=is_home_player)
        df = df.sort_values(by="at_bat_number", ascending=True)

        if is_home_player:
            df = df[df["delta_home_win_exp"] >= 0]
        else:
            df = df[df["delta_home_win_exp"] <= 0]

        df = df.head(plays)

        rows = [row for index, row in df.iterrows()]
        return async_run(Play, self, rows)

    def __str__(self) -> str:
        return f"{self._away.abbreviation} - {self._home.abbreviation}, Final: {self._away_score}-{self._home_score}, Date: {self._date}, GamePK: {self._game_pk}"

