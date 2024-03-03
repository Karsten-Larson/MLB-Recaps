import pandas as pd
import os

from functools import cache
from typing import List, Dict

class Team():
    _team_lookup: pd.DataFrame = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/team-info.csv'))

    # Speeds up and saves memory by caching the same type of objects
    @cache
    def __new__(cls, abbr: str):
        return super().__new__(cls)

    def __init__(self, abbr: str):
        self._abbr: str = abbr.upper()

        row: pd.DataFrame = Team._team_lookup.loc[Team._team_lookup["Abbreviation"] == self._abbr]
        self._team: str = row["Full Name"].values[0]
        self._team_id: int = row["Team ID"].values[0]

    @property
    def name(self) -> str:
        return self._team

    @property
    def abbreviation(self) -> str:
        return self._abbr

    @property
    def team_id(self) -> int:
        return self._team_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return False

        return self._abbr == other._abbr

    def __str__(self) -> str:
        return f"{self.__class__}@Name={self._team}:Abbreviation={self._abbr}:ID={self._team_id}"