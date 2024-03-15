from .scripts import get_highlights

from .date import Date
from .team import Team

if __name__ == "__main__":
    # Get teams for the search
    team = Team(input("Input team name: "))
    date = Date(input("Date MM/DD/YYYY: "))
    file_path = input("Downloads filepath: ")

    if not file_path.endswith("/"):
        file_path += "/"

    game_clips = get_highlights(team, date)

    for index, clips in enumerate(game_clips):
        # Download all highlight clips
        print(f"Game {index + 1}: {clips.plays[0].game}")

        clips.download(f"{file_path}{index}", verbose=True)
