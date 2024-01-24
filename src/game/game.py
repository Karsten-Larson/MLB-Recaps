from date.date_generator import DateGenerator
from typing import Type

class Game():
    def __init__(self, home: str, away: str, id: int, date: Type["Date"], data):
        self._home: str = home
        self._away: away = away
        self._id: int = id
        self._date: Type["Date"] = date
        self._data = data
        self._home_score = data.loc[:, "home_score"].max()
        self._away_score = data.loc[:, "away_score"].max()
    
    def getHome(self):
        return self._home

    def getAway(self):
        return self._away

    def getHomeScore(self):
        return self._home_score

    def getAwayScore(self):
        return self._away_score

    def getID(self):
        return self._date

    def getDate(self):
        return self._date

    def getData(self):
        return self._data

    def getGameHighlights(self, plays=10, team=None):
        df = self._data.copy()

        if play <= 0:
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
        return f"{self._away} - {self._home}, Final: {self._away_score}-{self._home_score}, Date: {self._date}, ID: {self._id}"

