# from mlbrecaps import Team, Date, DateRange, GameGenerator, Clips
from ..team import Team

def highlightGenerator(team: Team, dates: Date | DateRange, path: str, verbose: bool=True):
    # Type checking
    if not isinstance(team, Team):
        raise ValueError("team must be of type Team")
    
    if not (isinstance(dates, Date) or isinstance(dates, DateRange)):
        raise ValueError("dates must be of type Date or DateRange")

    if not isinstance(path, str):
        raise ValueError("path must be of type string")

    if not isinstance(verbose, bool):
        raise ValueError("verbose must be a boolean value")

    # get all games on that date
    games = GameGenerator(team, dates).games

    # Iterate over every game found
    for index, game in enumerate(games):
        # Determine whether the team is home or away
        homeRoad = game.road_status(team)

        # Get the top ten plays of the game
        homeHighlights = game.get_highlights(10, homeRoad) 
        homeClips = Clips(homeHighlights, homeRoad) # Generate clips of the plays from the home broadcast

        # Download all highlight clips
        if verbose:
            print(f"Game {index + 1}: {game}")

        homeClips.download(f"{path}{index}", verbose=verbose)


if __name__ == "__main__":
    # Get teams for the search
    team = Team("MIN")

    # Range of dates from September 17, 2023 to September 20, 2023
    dates = DateRange(Date(9, 17, 2023), Date(9, 20, 2023))

    highlightGenerator(team, dates, "/home/karsten/coding/python/recaps/videos/")
