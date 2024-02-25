from bs4 import BeautifulSoup

import requests
import json
import subprocess

from .play import Play

class Clip():

    def __init__(self, play: Play, broadcast_type: str | None=None):
        if not isinstance(play, Play):
            raise ValueError("Play must be a Play object")

        self.play: Play = play

        match broadcast_type: # Enforce broad_type types
            case "HOME" | "AWAY" | None:
                self.broadcast_type: str | None = broadcast_type
            case _:
                raise ValueError("BroadcastType must be None, \"HOME\", or \"AWAY\"")

        self.clip_url: str = self.__generate()

    def get_clip_url(self) -> str:
        return self.clip_url

    def __str__(self) -> str:
        return self.get_clip_url()

    def get_play(self) -> Play:
        return self.play

    # gets the url of the clip to be downloaded from the savant clip
    def __get_url(self, site_url: str) -> str:
        # Get the savant site
        site: requests.Response = requests.get(site_url)

        # Find the video element of the savant clip, find the source url of the clip
        soup= BeautifulSoup(site.text, features="lxml")
        video_obj = soup.find("video", id="sporty")

        if not video_obj:
            return ""

        source = video_obj.find('source')
        clip_url: str = source.get('src')

        # Return the source url of the clip so it can be downloaded later
        return clip_url


    # finds the savant clip based on the given at-bat information
    # row must be a pandas dataframe row
    def __generate(self) -> str:
        # load the given game's json file
        game_json = self.play.getGame().get_game_json()

        # find the broadcast type so it's always corresponding
        # to the given batter's home team's broadcast
        if self.broadcast_type:
            broadcast_type = self.broadcast_type
        elif self.play.getTopBot() == "TOP":
            broadcast_type = "AWAY"
        else:
            broadcast_type = "HOME"

        # with the play id find the url for the savant clip
        site_url = f"https://baseballsavant.mlb.com/sporty-videos?playId={self.play.getPlayID()}&videoType={broadcast_type}"
        clip_url = self.__get_url(site_url)

        # if the clip is alright return it
        if clip_url != "":
            return clip_url
        
        # if the clip is screwed up then it was a national tv game
        # return the correct national tv clip url
        site_url = f"https://baseballsavant.mlb.com/sporty-videos?playId={self.play.getPlayID()}&videoType=NETWORK"
        clip_url = self.__get_url(site_url)

        return clip_url

    def download(self, path: str, verbose: bool =False) -> None:
        # subprocess.run(["ffmpeg", "-i", self.clip_url, "-t", "60", "-c", "copy", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # create response object 
        # if a time out happens, try five more times before crashing the entire program
        for z in range(5):
            try:
                r = requests.get(self.clip_url, stream=True, timeout=60) 
                break
            except requests.exceptions.Timeout:
                print(f'Timeout has been raised. Link: {self.clip_url}')

        # download the file to the specific location
        # honestly copied and pasted code, can't say much else
        with open(path, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 

        if verbose:
            print(f"Successfully downloaded: {path}")