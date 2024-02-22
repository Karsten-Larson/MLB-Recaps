from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from player.player import Player
from clip.clip import Clip

from typing import Type, Union

def last10Homeruns(team: Type["Team"], dates: Union[Type["Date"], Type["DateRange"]]):
    games = GameGenerator(team, date).getGames()

    # Get the lineup of both games (in case of double header)
    lineup = set()

    # Reduce games into one lineup
    for game in games:
        for player_id in game.getTeamLineup(team): # Get lineup of the team only
            lineup.add(player_id)

    lineup = list(lineup)
    
    for player_id in lineup[::-1]:
        # Find player from the game
        player = Player(player_id, date.getYear())

        # Check if the player is a batter
        if not player.isBatter():
            continue

        # Check if the player has at least 10 homeruns 
        if player.getNumberOfHomeruns() < 10 or player.getNumberOfHomeruns() % 10 >= 5: 
            continue

        # Find his last 10 homeruns
        print(f"{player.getFullName()} had {player.getNumberOfHomeruns()} homeruns in {date.getYear()}!")
        homeruns = player.getHomeRuns()[-10:] # get last 10 homeruns

        # If their last homerun wasn't on that date, continue
        if homeruns[-1].getGame().getDate() != date:
            continue

        # Download all the homeruns
        for index, homerun in enumerate(homeruns):
            # Get whether twins were home or away in the given clip
            homeRoad = homerun.getGame().getHomeRoad(team)

            # Get the twins broadcast of the clip
            clip = Clip(homerun, homeRoad)
            print(homerun.getGame().getDate())

            # Download the clip
            clip.download(f"./videos/{player.getLastName()}{index:02d}.mp4", True)

    print(f"Successfully Completed")


if __name__ == "__main__":
    team = Team("ATL")
    date = Date.fromDate(10, 1, 2023)
    # date = Date.fromDate(10, 11, 2023)
    
    last10Homeruns(team, date)