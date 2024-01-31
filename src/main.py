from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from clip.clip import Clip

if __name__ == "__main__":
    teams = Team("MIN")
    dates = DateRange(Date.fromDate(9, 20, 2023), Date.fromDate(9, 22, 2023))

    games = GameGenerator(teams, dates).getGames()

    for index, game in enumerate(games):
        homeHighlights = game.getHomeTeamHighlights(10)
        homeClips = [Clip(highlight, "home") for highlight in homeHighlights]

        print(f"Game {index + 1}: {game}")

        for number, clip in enumerate(homeClips):
            clip.download(f"./videos/{index}{number:02d}.mp4", True)
