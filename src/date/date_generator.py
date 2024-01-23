from typing import Type, List
from datetime import datetime
from .date import Date
from copy import copy

class DateGenerator():

    @classmethod
    def today(cls) -> Type["Date"]:
        obj = Date(1,1,1)
        obj.date = datetime.now()

        return obj

    @classmethod
    def yesterday(cls) -> Type["Date"]:
        obj = cls.today()
        obj.prev()

        return obj

    @classmethod
    def tomorrow(cls) -> Type["Date"]:
        obj = cls.today()
        obj.next()

        return obj

    @classmethod
    def month(cls, month: int, year: int) -> List[Type["Date"]]:
        firstDate = Date(month, 1, year)
        dates = []

        while firstDate.date.month == month:
            dates.append(copy(firstDate))
            firstDate.next()

        return dates

if __name__ == "__main__":
    print("Ran")