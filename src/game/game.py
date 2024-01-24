from date.date_generator import DateGenerator

from typing import Type
import requests
import json

class Game():
    def __init__(self, home: str, away: str, game_pk: int, date: Type["Date"], gameData):
        self._home: str = home
        self._away: away = away
        self._game_pk: int = game_pk
        self._date: Type["Date"] = date
        self._game_data = gameData

        # finds the url of the game based on the game_pk information stored in the at-bat data
        game_url = f"https://baseballsavant.mlb.com/gf?game_pk={self._game_pk}"
        game = requests.get(game_url)

        # load the given game's json file
        self._game_json = json.loads(game.text)

        self._home_score = gameData.loc[:, "home_score"].max()
        self._away_score = gameData.loc[:, "away_score"].max()
    
    def getHome(self):
        return self._home

    def getAway(self):
        return self._away

    def getHomeScore(self):
        return self._home_score

    def getAwayScore(self):
        return self._away_score

    def getGamePK(self):
        return self.game_pk

    def getDate(self):
        return self._date

    def getData(self):
        return self._game_data

    def getGameJSON(self):
        return self._game_json

    def getGameHighlights(self, plays=10, team=None):
        df = self._game_data.copy()

        if plays <= 0:
            raise ValueError("Plays must be greater than 0")

        if team not in [None, "home", "away"]:
            raise ValueError("Team must be None, home, or away")

        # extra logic for when a home or away team is specified
        key = None if team else abs
        ascending = False if not team else (True, False)[team == "home"]

        # removes all non-events (balls, strikes, etc.)
        # then sorts for highest win expectancy for either team
        # then only keeps the top plays
        # also make sure the plays are in chronological order of the game
        df = df.loc[df.events.notnull()]
        df = df.sort_values(by="delta_home_win_exp", key=key, ascending=ascending)
        df = df.head(plays)
        df = df.sort_values(by="at_bat_number", ascending=True)

        return df

    def getHomeTeamHighlights(self, plays=10):
        return self.getGameHighlights(plays, "home")

    def getAwayTeamHighlights(self, plays=10):
        return self.getGameHighlights(plays, "away")

    def __str__(self) -> str:
        return f"{self._away} - {self._home}, Final: {self._away_score}-{self._home_score}, Date: {self._date}, GamePK: {self._game_pk}"

