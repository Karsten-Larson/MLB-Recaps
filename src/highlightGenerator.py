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

        home_highlights = game.getHomeTeamHighlights(10)
        home_clips = [Clip(highlight) for highlight in home_highlights]

        away_highlights = game.getAwayTeamHighlights(10)
        away_clips = [Clip(highlight) for highlight in away_highlights]

        print(f"Game {index + 1}: {game}")
        # print(*clips, sep="\n")

        for number, clip in enumerate(home_clips):
            clip.download(f"./videos/home{number}.mp4", True)

        for number, clip in enumerate(away_clips):
            clip.download(f"./videos/away{number}.mp4", True)
