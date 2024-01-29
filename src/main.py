from instabot.bot import Instabot
from teams.teams import Teams
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from clip.clip import Clip

if __name__ == "__main__":
    teams = Teams([142])
    # date = Date.fromDate(8, 6, 2023)
    dates = DateRange(Date.fromDate(8, 4, 2023), Date.fromDate(8, 6, 2023))

    games = [GameGenerator.fromGamePK(id) for id in GameGenerator(teams, dates).getIDs()]
    games.sort(key=lambda x: x.getDate())

    for index, game in enumerate(games):
        highlights = game.getHomeTeamHighlights(10)

        clips = [Clip(highlight) for index, highlight in highlights.iterrows()]

        print(f"Game {index + 1}: {game}")
        # print(*clips, sep="\n")

        for number, clip in enumerate(clips):
            clip.download(f"./videos/{index}{number}.mp4", True)
