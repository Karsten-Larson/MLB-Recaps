from typing import List, Literal, TYPE_CHECKING

from .play import Play
from .game import Game
from .clip import Clip
from .utils import async_run
import time

class Clips():
    def __init__(self, plays: List[Play] | Play, broadcast_type: Literal["HOME", "AWAY"] | None=None):
        match plays: # Enforce plays types
            case list():
                if len(plays) == 0 or not isinstance(plays[0], Play):
                    raise ValueError("A list of Play objects must be passed")

                self.plays: List[Play] = plays
            case Play():
                self.plays = [plays]
            case _:
                raise ValueError("A Play or list of Play objects must be passed")

        match broadcast_type: # Enforce broad_type types
            case "HOME" | "AWAY" | None:
                self.broadcast_type: str | None = broadcast_type
            case _:
                raise ValueError("BroadcastType must be None, \"HOME\", or \"AWAY\"")

        # Generate clip objects for each play passed
        self.clips = async_run(Clip, self.plays, self.broadcast_type)

    def get_plays(self) -> List[Play]:
        return self.plays

    def get_clips(self) -> List[Clip]:
        return self.clips

    def download(self, path: str, verbose: bool=False):
        paths = [f"{path}{index:03d}.mp4" for index in range(len(self.clips))]
        return async_run(Clip.download, self.clips, paths, verbose)