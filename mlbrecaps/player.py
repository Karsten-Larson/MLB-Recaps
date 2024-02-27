from __future__ import annotations

import pandas as pd
import io
import requests
import json

from typing import List, Dict, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Play

from .date_generator import DateGenerator
from .utils import async_run, dataframe_copy, dataframe_from_url

class Player():

    def __init__(self, player_id: int):
        self._player_id: int = player_id

        # Get player JSON information
        playerURL: str = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
        playerContent = requests.get(playerURL)
        self._player_json = json.loads(playerContent.text)["people"][0]

        # Player's name
        self._first_name: str = self._player_json["firstName"]
        self._last_name: str = self._player_json["lastName"]

        # Player's position
        self._primary_position: str = self._player_json["primaryPosition"]["name"]
        self._primary_position_abbr: str = self._player_json["primaryPosition"]["abbreviation"]

    def is_pitcher(self) -> bool:
        return self._primary_position_abbr == "P"

    def is_batter(self) -> bool:
        return not self.is_pitcher()

    def get_position(self) -> str:
        return self._primary_position

    def get_position_abbr(self) -> str:
        return self._primary_position_abbr

    def get_player_id(self) -> int:
        return self._player_id

    def get_season(self) -> int:
        return self._season

    def get_first_name(self) -> str:
        return self._first_name

    def get_last_name(self) -> str:
        return self._last_name

    def get_full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    # Lazy generate and save each season on call
    @dataframe_from_url
    def __get_homerun_data(self, season: int) -> pd.DataFrame:
        """
        Gets pandas dataframe information on all their homerun plays
        """
        return f"https://baseballsavant.mlb.com/statcast_search/csv?hfPT=&hfAB=home%5C.%5C.run%7C&hfGT=R%7C&hfPR=hit%5C.%5C.into%5C.%5C.play%7C&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea={season}%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&batters_lookup%5B%5D={self._player_id}&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&type=details&player_id={self._player_id}"

    # Encapsulates mutable data by making a copy
    @dataframe_copy
    def get_homerun_data(self, season: int) -> pd.DataFrame:
        return self.__get_homerun_data(season)

    def get_homerun_count(self, season: int) -> int:
        return len(self.__get_homerun_data(season).index)

    def get_homeruns(self, season: int | Date) -> List[Play]:
        from .game import Play, Game

        homerun_data = self.__get_homerun_data(season)
        # homerun_data.to_csv("./homeruns.csv")

        # if date:
            # homerun_data = homerun_data[homerun_data[]]

        games: List[Game] = async_run(Game, list(homerun_data["game_pk"]))
        rows = [row for index, row in homerun_data.iterrows()]

        return async_run(Play, games, rows)[::-1]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Player):
            return False

        return self._player_id == other._player_id

    def __hash__(self) -> int:
        return self._player_id

    def __str__(self) -> str:
        return f"{self.__class__}@PlayerID={self._player_id}:FirstName={self._first_name}:LastName={self._last_name}"