from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from player.player import Player
from clip.clip import Clip

from pybaseball import playerid_reverse_lookup, statcast_batter

if __name__ == "__main__":
    team = Team("MIN")
    date = Date.fromDate(10, 11, 2023)
    games = GameGenerator(team, date).getGames()
    
    for player_id in games[0].getHomeLineup():
        player = Player(player_id, date.getYear())

        print(f"{player.getFullName()} had {player.getNumberOfHomeruns()} homeruns in {date.getYear()}!")
        homeruns = player.getHomeRuns()[:1] # only getting the last three of every player

        for index, homerun in enumerate(homeruns):
            homeRoad = "HOME" if homerun.getGame().getHome() == "MIN" else "AWAY"
            clip = Clip(homerun, homeRoad)
            print(homerun.getGame().getDate())
            clip.download(f"./videos/{player.getLastName()}{len(homeruns)-index}.mp4", True)

    print(f"Successfully Completed")