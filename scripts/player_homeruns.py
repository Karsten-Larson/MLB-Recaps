from typing import List

from mlbrecaps import Player, Play, Clips

def player_homeruns(player_id: int, download_path: str, season: int=2023):
    player: Player = Player(player_id)

    homeruns: List[Play] = player.get_homeruns(season)

    clips: Clips = Clips(homeruns)
    clips.download(download_path, verbose=True)

if __name__ == "__main__":
    player_id = 621439
    path = "/home/karsten/coding/python/recaps/videos/0"

    player_homeruns(player_id, path, 2023)