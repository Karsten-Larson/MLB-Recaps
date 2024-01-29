from typing import Type

class Play():

    def __init__(self, game: Type["Game"], at_bat: int):
        self.game: Type["Game"] = game
        self.at_bat: int = at_bat
        self.play = game.getData().iloc[[at_bat]]
        self.inning_topbot: str = self.play.iloc[0].inning_topbot

    def getGame(self) -> Type["Game"]:
        return self.game

    def getAtBat(self) -> int:
        return self.at_bat

    def getPlayData(self):
        return self.play

    def getTopBot(self) -> str:
        return self.inning_topbot
