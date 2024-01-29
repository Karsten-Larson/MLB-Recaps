from date.date import Date
from date.date_range import DateRange
from .game import Game

import requests
import json
import pandas as pd
from pybaseball import statcast, statcast_single_game

from typing import Type, List, Union, Set

class GameGenerator():

    def __init__(self, teams: Type["Teams"], date: Union[Type["Date"], Type["DateRange"]]):
        self.teams: Type["Teams"] = teams
        self.date: Union[Type["Date"], Type["DateRange"]] = date
        self.ids: Set[int] = set()
        self._fromDates()

    @classmethod
    def fromGamePK(self, game_pk: int) -> Type["Game"]:
        df = statcast_single_game(game_pk)

        home = df.at[0, "home_team"]
        away = df.at[0, "away_team"]
        date = Date.fromDateString(str(df.at[0, "game_date"]))

        return Game(home, away, game_pk, date, df)     

    def _fromDates(self):
        if isinstance(self.date, DateRange):
            start_dt, end_dt = self.date.getDates()
        else:
            start_dt = end_dt = self.date

        games_url = [f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_dt.__str__()}&endDate={end_dt.__str__()}&sportId=1&teamId={teamId}" for teamId in self.teams.getTeams()]
        print(*games_url, sep="\n")
        date_jsons = [json.loads(requests.get(game_url).text) for game_url in games_url]

        for date_json in date_jsons:
            for date in date_json["dates"]:
                for game in date["games"]:
                    self.ids.add(game["gamePk"])

        print(self.ids)

    def getIDs(self) -> List[int]:
        # Only finds the unique game_pks for a given team (needed in case of a double header)
        return list(self.ids)
