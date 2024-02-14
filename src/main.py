from team.team import Team
from date.date import Date
from date.date_range import DateRange
from game.game_generator import GameGenerator
from clip.clip import Clip
from player.player import Player

if __name__ == "__main__":
    team = Team("MIN")
    date = Date.fromDate(6, 23, 2023)

    game = GameGenerator(team, date).getGames()[0]
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
