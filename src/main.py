from instabot.bot import Instabot
from teams.teams import Teams
from date.date import Date
from game.game_generator import GameGenerator
from clip.clip import Clip

if __name__ == "__main__":
    teams = Teams(["MIN"])
    date = Date.fromDate(8, 6, 2023)

    games = GameGenerator(teams, date)
    ids = games.getIDs()

    for index, id in enumerate(games.getIDs()):
        game = games.fromGamePK(id)
        highlights = game.getHomeTeamHighlights(10)

        clips = [Clip(highlight) for index, highlight in highlights.iterrows()]

        print(f"Game {index + 1}: {game}")
        # print(*clips, sep="\n")

        for number, clip in enumerate(clips):
            clip.download(f"./videos/{number}.mp4", True)
