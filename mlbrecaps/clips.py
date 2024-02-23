import asyncio

from typing import List, TYPE_CHECKING

from .play import Play
from .game import Game
from .clip import Clip

class Clips():
    def __init__(self, plays: List[Play] | Play, broadcastType: str | None=None):
        if isinstance(plays, list):
            if len(plays) == 0:
                raise ValueError("A list of play objects must be passed")

            self.plays: List[Play] = plays
        else:
            self.plays = [plays]

        if broadcastType and broadcastType.upper() not in ["HOME", "AWAY"]:
            raise ValueError("BroadcastType must be None, \"HOME\", or \"AWAY\"")

        self.broadcastType: str | None = broadcastType if not broadcastType else broadcastType.upper()

        async def generate():
            async def createClip(play):
                return Clip(play, self.broadcastType)

            tasks = [asyncio.create_task(createClip(play)) for play in self.plays]

            await asyncio.gather(*tasks)

            clips = [task.result() for task in tasks]
            return clips        

        self.clips = asyncio.run(generate())

    def getPlays(self) -> List[Play]:
        return self.plays

    def getClips(self) -> List[Clip]:
        return self.clips

    def download(self, path: str, verbose: bool=False):
        async def generate():            
            async def downloadClip(clip: Clip, path: str, verbose: bool):
                clip.download(path, verbose=verbose)

            tasks = []
            for index, clip in enumerate(self.clips):
                task = asyncio.create_task(downloadClip(clip, f"{path}{index:03d}.mp4", verbose))
                tasks.append(task)

            await asyncio.gather(*tasks)
        
        asyncio.run(generate())