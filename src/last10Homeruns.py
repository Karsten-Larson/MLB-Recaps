from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from player.player import Player
from clip.clip import Clip

if __name__ == "__main__":
    team = Team("MIN")
    date = Date.fromDate(9, 4, 2023)
    # date = Date.fromDate(10, 11, 2023)
    games = GameGenerator(team, date).getGames()

    # Get the lineup of both games (in case of double header)
    lineup = set()

    # Reduce games into one lineup
    for game in games:
        for player_id in game.getTeamLineup(team): # Get lineup of the twins only
            lineup.add(player_id)
    
    for player_id in lineup:
        # Find player from the game
        player = Player(player_id, date.getYear())

        # Check if the player had a multiple of 10 homeruns 
        if player.getNumberOfHomeruns() < 10 or player.getNumberOfHomeruns() % 10 != 0: 
            continue

        # Find his last 10 homeruns
        print(f"{player.getFullName()} had {player.getNumberOfHomeruns()} homeruns in {date.getYear()}!")
        homeruns = player.getHomeRuns()[-10:] # only getting the last 10 of every player

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