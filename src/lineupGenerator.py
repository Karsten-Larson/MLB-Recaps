from instabot.bot import Instabot
from teams.teams import Teams
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator

if __name__ == "__main__":
    teams = Teams([142])
    # date = Date.fromDate(8, 6, 2023)
    dates = DateRange(Date.fromDate(8, 4, 2023), Date.fromDate(8, 6, 2023))

    games = [GameGenerator.fromGamePK(id) for id in GameGenerator(teams, dates).getIDs()]
    games.sort(key=lambda x: x.getDate())

<<<<<<< HEAD:src/main.py
    for index, game in enumerate(games):
        highlights = game.getHomeTeamHighlights(10)

        clips = [Clip(highlight) for index, highlight in highlights.iterrows()]

        print(f"Game {index + 1}: {game}")
        # print(*clips, sep="\n")

        for number, clip in enumerate(clips):
            clip.download(f"./videos/{index}{number}.mp4", True)
=======
    for index, id in enumerate(games.getIDs()):
        game = games.fromGamePK(id)

        print(game.getHomeLineup())
>>>>>>> d9f8d255a4a76f8ccac97394cf9c35261f29fe43:src/lineupGenerator.py
