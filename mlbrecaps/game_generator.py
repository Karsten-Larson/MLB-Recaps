import requests
import json
import pandas as pd

from typing import List, Set, Tuple

from .team import Team
from .date import Date
from .date_range import DateRange
from .game import Game
from .utils import async_run

class GameGenerator():

    def __init__(self, teams: Team | List[Team], date: Date | DateRange | str | Tuple[int, int, int]):
        # Ensure teams is of correct type
        match teams:
            case list():
                if len(teams) == 0 or not isinstance(teams[0], Team):
                    raise ValueError("A list of Team objects must be passed")

                self.teams: List[Team] = teams
            case Team():
                self.teams = [teams]
            case _:
                raise ValueError("A Team or list of Team objects must be passed")

        # Ensure date is of correct type
        match date:
            case Date() | DateRange():
                self.date: Date | DateRange = date
            case tuple():
                try:
                    self.date = Date(*date)
                except ValueError:
                    raise ValueError("A Date or DateRange object must be passed")
            case _:
                try:
                    self.date = Date(date)
                except ValueError:
                    raise ValueError("A Date or DateRange object must be passed")

        self._ids: Set[int] = set()
        self.__from_dates()
        self._games: List[Game] | None = None

    def get_games(self) -> List[Game]:
        if self._games:
            return self._games.copy()

        # Generate every Game object from ids
        self._games = async_run(Game, list(self._ids))
        return self._games.copy()
        
    def __from_dates(self) -> None:
        if isinstance(self.date, DateRange):
            start_dt, end_dt = self.date.get_dates()
        else:
            start_dt = end_dt = self.date

        games_url = [f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_dt.to_formatted_string()}&endDate={end_dt.to_formatted_string()}&sportId=1&teamId={team.get_id()}" for team in self.teams]
        date_jsons = [json.loads(requests.get(game_url).text) for game_url in games_url]

        for date_json in date_jsons:
            for date in date_json["dates"]:
                for game in date["games"]:
                    self._ids.add(game["gamePk"])

    def get_ids(self) -> List[int]:
        # Only finds the unique game_pks for a given team (needed in case of a double header)
        return list(self._ids)

    def number_of_games(self) -> int:
        return len(self._ids)

