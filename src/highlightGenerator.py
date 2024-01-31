# from teams.teams import Teams
from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from clip.clip import Clip

if __name__ == "__main__":
    team = Team("MIN")
    dates = Date.fromDate(10, 11, 2023)

    games = GameGenerator(team, dates).getGames()

    for index, game in enumerate(games):
        homeRoad = "HOME" if game.getHome() == "MIN" else "AWAY"
        homeHighlights = game.getGameHighlights(10, homeRoad)
        homeClips = [Clip(highlight, homeRoad) for highlight in homeHighlights]

        print(f"Game {index + 1}: {game}")

        for number, clip in enumerate(homeClips):
            clip.download(f"./videos/{index}{number:02d}.mp4", True)
