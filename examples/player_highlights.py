from mlbrecaps import Player, GameGenerator, Team, Date, DateRange, Clips

def player_highlights(team: Team, player: Player, dates: Date | DateRange, path: str, verbose: bool=False):
    game = GameGenerator(team, dates).games[0]

    player_plays = game.get_player_highlights(player, 5)

    print(player_plays)

    clips = Clips(player_plays)
    clips.download(path, verbose=verbose)


if __name__ == "__main__":
    team = Team("MIN")
    player = Player(543243)
    dates = Date(9, 17, 2023)

    player_highlights(team, player, dates, "/home/karsten/coding/python/recaps/videos/0", True)