from typing import List

from .team import Team
from .player import Player
from .clips import Clips
from .date import Date
from .date_range import DateRange
from .game_generator import GameGenerator

def highlight_generator(team: Team, dates: Date | DateRange) -> List[Clips]:
    # Type checking
    if not isinstance(team, Team):
        raise ValueError("team must be of type Team")
    
    if not (isinstance(dates, Date) or isinstance(dates, DateRange)):
        raise ValueError("dates must be of type Date or DateRange")

    # get all games on that date
    games = GameGenerator(team, dates).games
    clips = []

    for game in games:
        # Determine whether the team is home or away
        homeRoad = game.road_status(team)

        # Get the top ten plays of the game
        homeHighlights = game.get_highlights(10, homeRoad) 
        clips.append(Clips(homeHighlights, homeRoad)) # Generate clips of the plays from the home broadcast

    return clips      

def player_highlights(team: Team, player: Player, dates: Date):
    # Type checking
    if not isinstance(team, Team):
        raise ValueError("team must be of type Team")
    
    if not isinstance(dates, Date):
        raise ValueError("dates must be of type Date or DateRange")

    game: Game = GameGenerator(team, dates).games[0]
    player_plays = game.get_player_highlights(player, 5)

    return Clips(player_plays)

def player_homeruns(player_id: Player | int, season: int=2023):
    if isinstance(player_id, Player):
        player: Player = player_id
    else:
        player = Player(player_id)

    homeruns: List[Play] = player.get_homeruns(season)

    return Clips(homeruns)
