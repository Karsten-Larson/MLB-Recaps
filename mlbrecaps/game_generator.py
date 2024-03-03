import requests
import json
import pandas as pd

# from multipledispatch import dispatch
from functools import singledispatchmethod, cache
from typing import List, Set, Tuple

from .team import Team
from .date import Date
from .date_range import DateRange
from .game import Game
from .utils import async_run

class GameGenerator():

    def __init__(self, teams: Team | List[Team], date: Date | DateRange | str | Tuple[int, int, int]):
        self.__set_teams(teams)
        self.__set_date(date)

        self._ids: Set[int] = self.__from_dates()

    @singledispatchmethod
    def __set_teams(self, teams: Team | List[Team]) -> None:
        raise ValueError("Teams must be a Team or list of Team object")

    @__set_teams.register(list)
    def _(self, teams: List[Team]) -> None:
        if len(teams) == 0 or not all(isinstance(team, Team) for team in teams):
            raise ValueError("A list of Team objects must be passed")

        self._teams: List[Team] = teams

    @__set_teams.register(Team)
    def _(self, teams: Team) -> None:
        self._teams = [teams]

    @singledispatchmethod
    def __set_date(self, date) -> None:
        raise ValueError("Invalid date must be of type Date, DateRange, str, or Tuple[int, int, int]")

    @__set_date.register(str)
    def _(self, date: str) -> None:
        try: 
            d = Date(date)
        except:
            raise ValueError("A valid date string of format %m/%d/%Y must be passed")

        self._date = DateRange(d, d)

    @__set_date.register(tuple)
    def _(self, date: Tuple[int, int, int]) -> None:
        try: 
            d = Date(*date)
        except:
            raise ValueError("A valid date tuple of format (month, day, year) must be passed")

        self._date = DateRange(d, d)

    @__set_date.register(Date)
    def _(self, date: Date) -> None:
        self._date: DateRange = DateRange(date, date)

    @__set_date.register(DateRange)
    def _(self, date: DateRange) -> None:
        self._date = date

    @property
    @cache
    def games(self) -> List[Game]:
        # Generate every Game object from ids
        games: List[Game] = async_run(Game, list(self._ids))
        games.sort(key=lambda game: game.date)

        return games
        
    def __from_dates(self) -> Set[int]:
        start_dt, end_dt = self._date.get_dates()

        games_url = [f"https://statsapi.mlb.com/api/v1/schedule?startDate={start_dt.to_formatted_string()}&endDate={end_dt.to_formatted_string()}&sportId=1&teamId={team.team_id}" for team in self._teams]
        date_jsons = [json.loads(requests.get(game_url).text) for game_url in games_url]

        # Put all game_pks into a set
        return {int(game["gamePk"]) for date_json in date_jsons for date in date_json["dates"] for game in date["games"]}

    @property
    def ids(self) -> List[int]:
        # Only finds the unique game_pks for a given team (needed in case of a double header)
        return list(self._ids)

    def __len__(self) -> int:
        return len(self._ids)

