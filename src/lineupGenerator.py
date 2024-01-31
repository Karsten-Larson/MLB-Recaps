from teams.teams import Teams
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from clip.clip import Clip

if __name__ == "__main__":
    teams = Teams([142])
    dates = Date.fromDate(10, 8, 2023)

    games = GameGenerator(teams, dates).getGames()

    for index, game in enumerate(games):
        homeRoad = "HOME" if game.getHome() == "MIN" else "AWAY"
        homeHighlights = game.getGameHighlights(10, homeRoad)
        homeClips = [Clip(highlight, homeRoad) for highlight in homeHighlights]

        print(f"Game {index + 1}: {game}")

        for number, clip in enumerate(homeClips):
            clip.download(f"./videos/{index}{number:02d}.mp4", True)
