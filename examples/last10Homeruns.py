from typing import Set, List

from mlbrecaps import Team, Date, Game, DateRange, GameGenerator, Player, Clip


def last10Homeruns(team: Team, dates: Date):
    games: List[Game] = GameGenerator(team, date).games
    season: int = date.year

    # Get all the players with a homerun in all the games of the day
    lineup: Set[Player] = set()

    for game in games:
        homers: Set[int] = set(game.homers)
        for player in Player.generate_players(game.get_lineup(team)):
            if player.player_id in homers:
                lineup.add(player)

    print(*[player.player_id for player in lineup], sep=", ")

    for player in lineup:
        # Find his last 10 homeruns
        print(
            f"{player.full_name} had {player.get_homerun_count(season)} homeruns in {date.year}!"
        )

        # Get all homeruns
        homeruns = player.get_homeruns(season)
        last_ten_index = 0

        for index in range(round(player.get_homerun_count(season), -1) - 1, 0, -10):
            # If their last homerun wasn't on that date, continue
            if homeruns[index].game.date != date:
                last_ten_index = index
                break

        if last_ten_index == 0:
            continue

        # Download all the homeruns
        for index, homerun in enumerate(homeruns[last_ten_index-9:last_ten_index]):
            # Get whether team were home or away in the given clip
            homeRoad: str = homerun.game.road_status(team)

            # Get the home broadcast of the clip
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
