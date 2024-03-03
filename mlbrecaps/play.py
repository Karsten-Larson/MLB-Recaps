from __future__ import annotations

import pandas as pd
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class Play():

    def __init__(self, game: Game, row):
        self._game: Game = game
        self._at_bat: int = row.at_bat_number
        self._play: pd.DataFrame = row
        self._pitch_number: int = row.pitch_number
        self._batter: str = row.player_name
        self._event: str = row.description
        self._description: str = row.des
        self._inning_topbot: str = row.inning_topbot

        if self._inning_topbot == "Top":
            team = self._game.home_json
        else:
            team = self._game.away_json

        # filter the json file to find the at bat, this will help find the play id
        team = [x for x in team if x["ab_number"] == self._at_bat]

        # sorts the at bat by pitch number, highest number is the last pitch of the at bat
        team.sort(key=lambda item: item["pitch_number"], reverse=True)
        self._play_id: str = team[0]["play_id"]

    @property
    def game(self) -> Game:
        return self._game

    @property
    def at_bat(self) -> int:
        return self._at_bat

    @property
    def play_data(self) -> pd.DataFrame:
        return self._play.copy()

    @property
    def inning_topbot(self) -> str:
        return self._inning_topbot

    @property
    def batter(self) -> str:
        return self._batter

    @property
    def event(self) -> str:
        return self._event

    @property
    def description(self) -> str:
        return self._description

    @property
    def play_id(self) -> str:
        return self._play_id

    def __str__(self):
        return f"{self.__class__}@Game={self._game}:atBat={self._at_bat}:Batter={self._batter}:Description={self._description}:topBot={self._inning_topbot}"
