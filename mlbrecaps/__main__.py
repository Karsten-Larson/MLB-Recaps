from typing import List
from pathlib import Path

from .scripts import get_highlights

from .date import Date
from .team import Team
from .clips import Clips

if __name__ == "__main__":
    # Get teams for the search
    team: Team = Team(input("Input team name: "))
    date: Date = Date(input("Date MM/DD/YYYY: "))
    file_path: Path = Path(input("Downloads filepath: "))

    game_clips: List[Clips] = get_highlights(team, date)

    for index, clips in enumerate(game_clips):
        # Download all highlight clips
        print(f"Game {index + 1}: {clips.plays[0].game}")

        dir_path: Path = file_path / f"{index:03d}"
        dir_path.mkdir(exist_ok=True)

        clips.download(dir_path, verbose=True)
