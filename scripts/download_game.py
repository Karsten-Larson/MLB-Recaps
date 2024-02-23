from mlbrecaps import Team, Game, GameGenerator, Date, DateRange, Player, Clips
import time

if __name__ == "__main__":
    team = Team("MIN")
    date = Date(9, 30, 2023)

    games = GameGenerator(team, date).getGames()
    game = games[0]

    plays = game.getHighlights(10, game.getHomeRoad(team))
    clips = Clips(plays, game.getHomeRoad(team))

    clips.download("/home/karsten/coding/python/recaps/videos", verbose=True)
