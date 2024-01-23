from .date import Date
from .date_range import DateRange

from typing import Type
from datetime import datetime
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
    def month(cls, month: int, year: int) -> Type["DateRange"]:
        start_dt = Date(month, 1, year)

        # set the end date to the end of the month
        end_dt = copy(start_dt)
        end_dt.next(28)

        # check if it is still in the month then go one back
        while end_dt.date.month == month:
            end_dt.next()

        end_dt.prev()

        return DateRange(start_dt, end_dt)

if __name__ == "__main__":
    print("Ran")