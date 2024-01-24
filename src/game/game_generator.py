from date.date import Date
from date.date_range import DateRange
from .game import Game

import pandas as pd
from pybaseball import statcast, statcast_single_game

from typing import Type, List, Union

class GameGenerator():

    def __init__(self, teams: Type["Teams"], date: Union[Type["Date"], Type["DateRange"]]):
        self.teams: Type["Teams"] = teams
        self.date: Union[Type["Date"], Type["DateRange"]] = date
        self._fromDates()

    def fromGamePK(self, game_pk: int) -> Type["Game"]:
        df = self.df.loc[self.df.game_pk == game_pk]

        home = df.at[0, "home_team"]
        away = df.at[0, "away_team"]
        date = Date.fromDateString(str(df.at[0, "game_date"]))

        return Game(home, away, game_pk, date, df)     

    def _fromDates(self):
        if isinstance(self.date, DateRange):
            start_dt, end_dt = self.date.getDates()
        else:
            start_dt = end_dt = self.date

        # Finds the data for all teams on a given date
        self.df = pd.concat([statcast(start_dt=start_dt.__str__(), end_dt=end_dt.__str__(), team=team, verbose=False) for team in self.teams.getTeams()])

        # self.df.to_csv("game.csv")

    def getIDs(self) -> List[int]:
        # Only finds the unique game_pks for a given team (needed in case of a double header)
        return list(self.df.game_pk.unique())
