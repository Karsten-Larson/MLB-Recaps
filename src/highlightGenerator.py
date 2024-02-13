from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from clip.clip import Clip

if __name__ == "__main__":
    # Get teams for the search
    team = Team("MIN")
    dates = Date.fromDate(10, 11, 2023)

    # get all games on that date
    games = GameGenerator(team, dates).getGames()

    # Iterate over every game found
    for index, game in enumerate(games):
        # Determine whether the Twins are home or away
        homeRoad = "HOME" if game.getHome() == "MIN" else "AWAY"

        # Get the top ten plays Twins highlight of the game
        homeHighlights = game.getGameHighlights(10, homeRoad) 
        homeClips = [Clip(highlight, homeRoad) for highlight in homeHighlights] # Generate clips of the plays from the Twins broadcast

        # Download all highlight clips
        print(f"Game {index + 1}: {game}")

        for number, clip in enumerate(homeClips):
            clip.download(f"./videos/{index}{number:02d}.mp4", True)
