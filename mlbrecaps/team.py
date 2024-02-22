import pandas as pd
import os

from typing import List

class Team():
    teamLookup: pd.DataFrame = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/team-info.csv'))

    def __init__(self, abbr: str):
        self.abbr: str = abbr.upper()

        row: pd.DataFrame = Team.teamLookup.loc[Team.teamLookup["Abbreviation"] == abbr]
        self.team: str = row["Full Name"].values[0]
        self.teamID: int = row["Team ID"].values[0]

    def getName(self) -> str:
        return self.team

    def getAbbreviation(self) -> str:
        return self.abbr

    def getID(self) -> int:
        return self.teamID

    def __str__(self) -> str:
        return f"{self.__class__}@Name={self.team}:Abbreviation={self.abbr}:ID={self.teamID}"