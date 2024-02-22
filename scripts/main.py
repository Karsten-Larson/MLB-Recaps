from mlbrecaps import Team, Date, GameGenerator, Player

if __name__ == "__main__":
    team = Team("MIN")
    date = Date.fromDate(4, 18, 2023)

    game = GameGenerator(team, date).getGames()[0]
    print(game)
    print(game.getGamePK())
    exit()
    player = Player(543877, 2023)

    plays = game.getPlayerHighlights(player)

    for play in plays:
        print(play)


    # for index, game in enumerate(games):
    #     homeHighlights = game.getHomeTeamHighlights(10)
    #     homeClips = [Clip(highlight, "home") for highlight in homeHighlights]

    #     print(f"Game {index + 1}: {game}")

    #     for number, clip in enumerate(homeClips):
    #         clip.download(f"./videos/{index}{number:02d}.mp4", True)
