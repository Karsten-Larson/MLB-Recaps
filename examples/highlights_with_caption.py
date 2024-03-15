from mlbrecaps import GameGenerator, Team, Date, DateRange, Clips

# team and date info
team = Team("NYY")
dates = Date(7, 4, 2023)

# Can also be a range of dates
# dates = DateRange(Date(7, 4, 2023), Date(7, 5, 2023))

# get all games on that date (in case of doubleheader or range of dates)
games = GameGenerator(team, dates).games

# path of folder to download to
path = "/path/to/folder/"

# Iterate over every game found
for index, game in enumerate(games):
   # Determine whether the team is home or away
   homeRoad = game.road_status(team)

   # Get the top ten plays of the game
   homeHighlights = game.get_highlights(10, homeRoad) 
   homeClips = Clips(homeHighlights, homeRoad) # Generate clips of the plays from the home broadcast

   # Download all highlight clips
   if verbose:
       print(f"Game {index + 1}: {game}")

   with open(f"{path}{index}.txt", "w") as f:
       f.write(str(game)) # caption of videos
       # other data about the game is available to be put in caption

   # Download all the clips to a file path
   homeClips.download(f"{path}{index}", verbose=True)