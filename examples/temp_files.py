from typing import List

import tempfile
from pathlib import Path

from mlbrecaps import Team, Date, get_highlights, Clips

if __name__ == "__main__":
    # Get teams for the search
    team: Team = Team(input("Input team name: "))
    date: Date = Date(input("Date MM/DD/YYYY: "))

    game_clips: List[Clips] = get_highlights(team, date)

    with tempfile.TemporaryDirectory() as temp_dir:
        file_path: Path = Path(temp_dir)

        for index, clips in enumerate(game_clips):
            # Download all highlight clips
            print(f"Game {index + 1}: {clips.plays[0].game}")

            dir_path: Path = file_path / f"{index:03d}"
            dir_path.mkdir(exist_ok=True)

            output: List[Path] = clips.download(dir_path, verbose=True)

        input("Press enter to delete files: ")
