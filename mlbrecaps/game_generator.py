import requests
import json
import pandas as pd

from typing import List, Set

from .team import Team
from .date import Date
from .date_range import DateRange
from .game import Game

class GameGenerator():

    def __init__(self, teams: Team | List[Team], date: Date | DateRange):
        # Check if valid a valid team object list or team object is passed
        if isinstance(teams, list):
            if len(teams) == 0:
                raise ValueError("A list of Team objects must be passed")

            self.teams: List[Team] = teams
        else:
            self.teams = [teams]

        self.date: Date | DateRange = date
        self.ids: Set[int] = set()
        self._fromDates()

    def getGames(self) -> List[Game]:
        games = [Game(gameID) for gameID in list(self.ids)]   
        games.sort(key=lambda x: x.getDate())

        return games

    def _fromDates(self) -> None:
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
