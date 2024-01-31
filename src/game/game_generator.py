from date.date import Date
from date.date_range import DateRange
from .game import Game

import requests
import json
import pandas as pd

from typing import Type, List, Union, Set

class GameGenerator():

    def __init__(self, teams: Type["Team"], date: Union[Type["Date"], Type["DateRange"]]):
        if isinstance(teams, list):
            self.teams: List[Type["Teams"]] = teams
        else:
            self.teams: Type["Teams"] = [teams]

        self.date: Union[Type["Date"], Type["DateRange"]] = date
        self.ids: Set[int] = set()
        self._fromDates()

    def getGames(self) -> List[Type["Game"]]:
        games = [Game(gameID) for gameID in list(self.ids)]   
        games.sort(key=lambda x: x.getDate())

        return games

    def _fromDates(self):
        if isinstance(self.date, DateRange):
            start_dt, end_dt = self.date.getDates()
        else:
            start_dt = end_dt = self.date

        games_url = [f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_dt.__str__()}&endDate={end_dt.__str__()}&sportId=1&teamId={team.getID()}" for team in self.teams]
        date_jsons = [json.loads(requests.get(game_url).text) for game_url in games_url]

        for date_json in date_jsons:
            for date in date_json["dates"]:
                for game in date["games"]:
                    self.ids.add(game["gamePk"])

    def getIDs(self) -> List[int]:
        # Only finds the unique game_pks for a given team (needed in case of a double header)
        return list(self.ids)
