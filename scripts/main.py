from mlbrecaps import Team, Date, GameGenerator, Player

if __name__ == "__main__":
    team = Team("MIN")
    date = Date(4, 18, 2023)

    game = GameGenerator(team, date).games[0]
    print(game)
    print(game.game_pk)
    exit()
    player = Player(543877)

    plays = game.get_player_highlights(player)

    for play in plays:
        print(play)

