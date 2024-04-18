from typing import List, Literal
from functools import singledispatchmethod
from pathlib import Path

from .play import Play
from .game import Game
from .clip import Clip
from .utils import async_run


class Clips():
    """Container class for working with and generating multiple clips from a list of plays"""

    def __init__(self, plays: List[Play] | Play, broadcast_type: Literal["HOME", "AWAY"] | None = None):
        self.__set_plays(plays)

        match broadcast_type:  # Enforce broad_type types
            case "HOME" | "AWAY" | None:
                self._broadcast_type: str | None = broadcast_type
            case _:
                raise ValueError(
                    "BroadcastType must be None, \"HOME\", or \"AWAY\"")

        # Generate clip objects for each play passed
        self._clips = async_run(Clip, self._plays, self._broadcast_type)

    @singledispatchmethod
    def __set_plays(self, plays) -> None:
        raise ValueError("A Play or list of Play objects must be passed")

    @__set_plays.register(list)
    def _(self, plays: List[Play]) -> None:
        if len(plays) == 0 or not isinstance(plays[0], Play):
            raise ValueError("A list of Play objects must be passed")

        self._plays: List[Play] = plays

    @__set_plays.register(Play)
    def _(self, plays: Play) -> None:
        self._plays = [plays]

    @property
    def plays(self) -> List[Play]:
        return self._plays

    @property
    def clips(self) -> List[Clip]:
        return self._clips

    @property
    def broadcast_type(self) -> str:
        return self._broadcast_type

    def download(self, dir_path: str | Path, verbose: bool = False) -> List[Path]:
        """Download all clips into a single directory"""
        # Convert path string to Path object
        dir_path: Path = dir_path if isinstance(
            dir_path, Path) else Path(dir_path)
        dir_path.mkdir(exist_ok=True, parents=True)

        # Get all paths for the mp4s
        paths: List[Path] = [
            dir_path / f"{index:04d}.mp4" for index in range(len(self._clips))]

        # Create all paths in memory if they don't exist
        for p in paths:
            p.touch()

        # Download all clips and return the download paths
        return async_run(Clip.download, self._clips, paths, verbose)
