from date.date_generator import DateGenerator
from typing import Type

class Game():
    def __init__(self, home: str, away: str, id: int, date: Type["Date"]):
        self.home: str = home
        self.away: away = away
        self.id: int = id
        self.date: Type["Date"] = date

    def __str__(self) -> str:
        return f"{self.away} - {self.home}, date: {self.date}, id: {self.id}"


if __name__ == "__main__":
    date = DateGenerator.today()
    game = Game("Twins", "Mets", 1893132, date)

    print(game)