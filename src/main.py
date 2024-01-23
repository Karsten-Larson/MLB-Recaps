from copy import copy
from instabot.bot import Instabot
from teams.teams import Teams
from date.date import Date
from game.game_generator import GameGenerator

if __name__ == "__main__":
    date = Date(9, 1, 2023)
    teams = Teams(["MIN"])
    games = GameGenerator.fromDate(teams, date)

    print(games[0])
