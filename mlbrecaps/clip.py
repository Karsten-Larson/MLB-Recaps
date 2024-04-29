from bs4 import BeautifulSoup

import requests
import cloudscraper
from pathlib import Path

from .play import Play


class Clip():
    """A wrapper class for Play that allows for plays to be downloaded"""

    def __init__(self, play: Play, broadcast_type: str | None = None):
        if not isinstance(play, Play):
            raise ValueError("Play must be a Play object")

        self._play: Play = play

        match broadcast_type:  # Enforce broad_type types
            case "HOME" | "AWAY" | None:
                self.broadcast_type: str | None = broadcast_type
            case _:
                raise ValueError(
                    "BroadcastType must be None, \"HOME\", or \"AWAY\"")

        self._clip_url: str = self.__generate()
        print(self._clip_url)

    @property
    def clip_url(self) -> str:
        return self._clip_url

    def __str__(self) -> str:
        return self.clip_url

    @property
    def play(self) -> Play:
        return self._play

    def __get_url(self, site_url: str) -> str:
        """
        Gets the url of the clip to be downloaded from the savant clip
        """
        # Get the savant site
        site: requests.Response = requests.get(site_url)

        # Find the video element of the savant clip, find the source url of the clip
        soup = BeautifulSoup(site.text, features="lxml")
        video_obj = soup.find("video", id="sporty")

        if not video_obj:
            return ""

        source = video_obj.find('source')
        clip_url: str = source.get('src')

        # Return the source url of the clip so it can be downloaded later
        return clip_url

    def __generate(self) -> str:
        """
        Generates a savant clip based on the given at-bat information

        Row must be a pandas dataframe row.
        """

        # find the broadcast type so it's always corresponding
        # to the given batter's home team's broadcast
        if self.broadcast_type:
            broadcast_type = self.broadcast_type
        elif self._play.inning_topbot == "TOP":
            broadcast_type = "AWAY"
        else:
            broadcast_type = "HOME"

        # with the play id find the url for the savant clip
        site_url = f"https://baseballsavant.mlb.com/sporty-videos?playId={self._play.play_id}&videoType={broadcast_type}"
        clip_url = self.__get_url(site_url)

        # if the clip is alright return it
        if clip_url != "":
            return clip_url

        # if the clip is screwed up then it was a national tv game
        # return the correct national tv clip url
        site_url = f"https://baseballsavant.mlb.com/sporty-videos?playId={self._play.play_id}&videoType=NETWORK"
        clip_url = self.__get_url(site_url)

        return clip_url

    def download(self, path: str | Path, verbose: bool = False) -> Path:
        path = path if isinstance(path, Path) else Path(path)

        # create response object
        try:
            r = cloudscraper.create_scraper().get(self._clip_url, stream=True, timeout=60)
        except requests.exceptions.Timeout:
            print(f'Timeout has been raised. Link: {self._clip_url}')

        # Download video
        open(path, "wb").write(r.content)

        # State the video was successfully downloaded (not always the case lol)
        if verbose:
            print(f"Successfully downloaded: {path.absolute()}")

        return path
