from __future__ import annotations

import pandas as pd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class Play():

    def __init__(self, game: Game, row):
        self.game: Game = game
        self.at_bat: int = row.at_bat_number
        self.play: pd.DataFrame = row
        self.pitch_number: int = row.pitch_number
        self.batter: str = row.player_name
        self.description: str = row.description
        self.inning_topbot: str = row.inning_topbot

        if self.inning_topbot == "Top":
            team = self.game.getHomeJSON()
        else:
            team = self.game.getAwayJSON()

        # filter the json file to find the at bat, this will help find the play id
        team = [x for x in team if x["ab_number"] == self.at_bat]

        # sorts the at bat by pitch number, highest number is the last pitch of the at bat
        team.sort(key=lambda item: item["pitch_number"], reverse=True)
        self.playID: str = team[0]["play_id"]

    def getGame(self) -> Game:
        return self.game

    def getAtBat(self) -> int:
        return self.at_bat

    def getPlayData(self) -> pd.DataFrame:
        return self.play.copy()

    def getTopBot(self) -> str:
        return self.inning_topbot

    def getBatter(self) -> str:
        return self.batter

    def getDescription(self) -> str:
        return self.description

    def getPlayID(self) -> str:
        return self.playID

    def __str__(self):
        return f"{self.__class__}@Game={self.game}:atBat={self.at_bat}:Batter={self.batter}:Description={self.description}:topBot={self.inning_topbot}"
