from date.date import Date
from .game import Game

import pandas as pd
from pybaseball import statcast, statcast_single_game

from typing import Type, List

class GameGenerator():

    @classmethod
    def fromID(cls, id: int) -> Type["Game"]:
        return statcast_single_game(id)

    @classmethod
    def fromDate(cls, teams: Type["Teams"], date: Type["Date"]) -> List[Type["Game"]]:
        # Finds the data for all teams on a given date
        df = pd.concat([statcast(start_dt=date.__str__(), team=team, verbose=True) for team in teams.getTeams()])

        # Only finds the unique game_pks for a given team (needed in case of a double header)
        game_pks = list(df.game_pk.unique())

        # Returns the list of game ids
        return [cls.fromID(id) for id in game_pks]

    @classmethod
    def fromDates(cls, teams: Type["Teams"], dates: Type["DateRange"]) -> List[Type["Game"]]:
        pass
