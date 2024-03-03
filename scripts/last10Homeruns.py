from typing import Set, List

from mlbrecaps import Team, Date, DateRange, GameGenerator, Player, Clip

def last10Homeruns(team: Team, dates: Date | DateRange):
    games: List[Game] = GameGenerator(team, date).games

    # Get the lineup of both games (in case of double header)
    lineup: Set[int] = set()

    # Reduce games into one lineup
    for game in games:
        for player_id in game.get_lineup(team): # Get lineup of the team only
            lineup.add(player_id)
    
    for player_id in lineup:
        # Find player from the game
        player: Player = Player(player_id, date.year)

        # Check if the player is a batter
        if not player.is_batter():
            continue

        # Check if the player has at least 10 homeruns 
        if player.get_homerun_count() < 10: 
            continue

        # Find his last 10 homeruns
        print(f"{player.get_full_name()} had {player.get_homerun_count()} homeruns in {date.year}!")
        homeruns = player.get_homeruns()[-10:] # get last 10 homeruns

        # If their last homerun wasn't on that date, continue
        if homeruns[-1].game.date != date:
            continue

        # Download all the homeruns
        for index, homerun in enumerate(homeruns):
            # Get whether twins were home or away in the given clip
            homeRoad: str = homerun.game.road_status(team)

            # Get the twins broadcast of the clip
            clip: Clip = Clip(homerun, homeRoad)
            print(homerun.game.date)

            # Download the clip
            clip.download(f"./videos/{player.last_name}{index:02d}.mp4", True)

    print(f"Successfully Completed")


if __name__ == "__main__":
    team = Team("ATL")
    date = Date(10, 1, 2023)
    # date = Date(10, 11, 2023)
    
    last10Homeruns(team, date)