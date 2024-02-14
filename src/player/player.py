from typing import Type, List

from date.date_generator import DateGenerator
from game.game import Game
from game.play import Play

import pandas as pd
import io
import requests
import json

class Player():

    def __init__(self, playerID: int, season: int):
        self.playerID: int = playerID
        self.season: int = season

        # Get player JSON information
        playerURL = f"https://statsapi.mlb.com/api/v1/people/{playerID}"
        playerContent = requests.get(playerURL)
        self.playerJSON = json.loads(playerContent.text)["people"][0]

        # Player's name
        self.firstName = self.playerJSON["firstName"]
        self.lastName = self.playerJSON["lastName"]

        # Player's position
        self.primaryPosition = self.playerJSON["primaryPosition"]["name"]
        self.primaryPositionAbbr = self.playerJSON["primaryPosition"]["abbreviation"]

        # Get CSV information on all their homerun plays
        homerunURL = f"https://baseballsavant.mlb.com/statcast_search/csv?hfPT=&hfAB=home%5C.%5C.run%7C&hfGT=R%7C&hfPR=hit%5C.%5C.into%5C.%5C.play%7C&hfZ=&hfStadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea={season}%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&batters_lookup%5B%5D={playerID}&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&type=details&player_id={playerID}"
        homerunCSV = requests.get(homerunURL).content

        self.homerunData = pd.read_csv(io.StringIO(homerunCSV.decode('utf-8')))

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

    def getHomeRuns(self) -> List[Type["Play"]]:
        return [Play(Game(row.game_pk), row) for index, row in self.homerunData.iterrows()][::-1]

    def __str__(self) -> str:
        return f"{__class__}@PlayerID={self.playerID}:FirstName={self.firstName}:LastName={self.lastName}"