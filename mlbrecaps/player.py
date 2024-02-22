from __future__ import annotations

import pandas as pd
import io
import requests
import json

from typing import List, cast, TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Play

from .date_generator import DateGenerator

class Player():

    def __init__(self, playerID: int, season: int):
        self.playerID: int = playerID
        self.season: int = season

        # Get player JSON information
        playerURL: str = f"https://statsapi.mlb.com/api/v1/people/{playerID}"
        playerContent = requests.get(playerURL)
        self.playerJSON = json.loads(playerContent.text)["people"][0]

        # Player's name
        self.firstName: str = self.playerJSON["firstName"]
        self.lastName: str = self.playerJSON["lastName"]

        # Player's position
        self.primaryPosition: str = self.playerJSON["primaryPosition"]["name"]
        self.primaryPositionAbbr: str = self.playerJSON["primaryPosition"]["abbreviation"]

        # Get CSV information on all their homerun plays
        homerunURL: str = f"https://baseballsavant.mlb.com/statcast_search/csv?hfPT=&hfAB=home%5C.%5C.run%7C&hfGT=R%7C&hfPR=hit%5C.%5C.into%5C.%5C.play%7C&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea={season}%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&batters_lookup%5B%5D={playerID}&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&type=details&player_id={playerID}"
        homerunCSV: bytes = requests.get(homerunURL).content

        self.homerunData: pd.DataFrame = pd.read_csv(io.StringIO(homerunCSV.decode('utf-8')))

    def isPitcher(self) -> bool:
        return self.primaryPositionAbbr == "P"

    def isBatter(self) -> bool:
        return not self.isPitcher()

    def getPosition(self) -> str:
        return self.primaryPosition

    def getPositionAbbr(self) -> str:
        return self.primaryPositionAbbr

    def getPlayerID(self) -> int:
        return self.playerID

    def getSeason(self) -> int:
        return self.season

    def getFirstName(self) -> str:
        return self.firstName

    def getLastName(self) -> str:
        return self.lastName

    def getFullName(self) -> str:
        return f"{self.firstName} {self.lastName}"

    def getData(self) -> pd.DataFrame:
        return self.homerunData.copy()

    def getNumberOfHomeruns(self) -> int:
        return len(self.homerunData.index)

    def getHomeRuns(self) -> List[Play]:
        from .game import Play, Game

        return [Play(Game(row.game_pk), row) for index, row in self.homerunData.iterrows()][::-1]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Player):
            return False

        other: Player = cast(Player, o)

        return self.playerID == other.playerID

    def __hash__(self) -> int:
        return self.playerID

    def __str__(self) -> str:
        return f"{self.__class__}@PlayerID={self.playerID}:FirstName={self.firstName}:LastName={self.lastName}"