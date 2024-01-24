import requests
from bs4 import BeautifulSoup
import json
import subprocess

class Clip():

    def __init__(self, row):
        self.game_pk: str = row.game_pk
        self.at_bat: int = row.at_bat_number
        self.inning_topbot: str = row.inning_topbot
        self.clip_url: str = self._generate()

    def getGamePK(self) -> str:
        return self.game_pk

    def getAtBat(self) -> str:
        return self.at_bat

    def getClipURL(self) -> str:
        return self.clip_url

    def __str__(self):
        return self.getClipURL()

    # gets the url of the clip to be downloaded from the savant clip
    def _get_url(self, site_url: str) -> str:
        # Get the savant site
        site = requests.get(site_url)

        # Find the video element of the savant clip, find the source url of the clip
        soup = BeautifulSoup(site.text, features="lxml")
        video_obj = soup.find("video", id="sporty")
        clip_url = video_obj.find('source').get('src')

        # Return the source url of the clip so it can be downloaded later
        return clip_url


    # finds the savant clip based on the given at-bat information
    # row must be a pandas dataframe row
    def _generate(self) -> str:
        # finds the url of the game based on the game_pk information stored in the at-bat data
        game_url = f"https://baseballsavant.mlb.com/gf?game_pk={self.game_pk}"
        game = requests.get(game_url)

        # load the given game's json file
        game_json = json.loads(game.text)

        # find the broadcast type so it's always corresponding
        # to the given batter's home team's broadcast
        if self.inning_topbot == "Top":
            team = game_json["team_home"]
            broadcast_type = "&videoType=AWAY"
        else:
            team = game_json["team_away"]
            broadcast_type = "&videoType=HOME"

        # filter the json file to find the at bat, this will help find the play id
        team = list(filter(lambda item: item["ab_number"] == self.at_bat, team))

        # sorts the at bat by pitch number, highest number is the last pitch of the at bat
        team.sort(key=lambda item: item["pitch_number"], reverse=True)
        pitch = team[0]

        # with the play id find the url for the savant clip
        site_url = f"https://baseballsavant.mlb.com/sporty-videos?playId={pitch['play_id']}{broadcast_type}"
        clip_url = self._get_url(site_url)

        # if the clip is alright return it
        if clip_url != "":
            return clip_url
        
        # if the clip is screwed up then it was a national tv game
        # return the correct national tv clip url
        site_url = f"https://baseballsavant.mlb.com/sporty-videos?playId={pitch['play_id']}&videoType=NETWORK"
        clip_url = self._get_url(site_url)

        return clip_url

    def download(self, path, verbose=False):
        # subprocess.run(["ffmpeg", "-i", self.clip_url, "-t", "60", "-c", "copy", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # create response object 
        # if a time out happens, try five more times before crashing the entire program
        for z in range(5):
            try:
                r = requests.get(self.clip_url, stream=True, timeout=60) 
                break
            except Timeout:
                print(f'Timeout has been raised. Link: {self.clip_url}')

        # download the file to the specific location
        # honestly copied and pasted code, can't say much else
        with open(path, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 

        if verbose:
            print(f"Successfully downloaded: {path}")