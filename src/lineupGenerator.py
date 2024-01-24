from instabot.bot import Instabot
from teams.teams import Teams
from date.date import Date
from game.game_generator import GameGenerator

if __name__ == "__main__":
    teams = Teams(["MIN"])
    date = Date.fromDate(8, 6, 2023)

    games = GameGenerator(teams, date)
    ids = games.getIDs()

    for index, id in enumerate(games.getIDs()):
        game = games.fromGamePK(id)

        print(game.getHomeLineup())
