from datetime import datetime
from copy import copy

from .date import Date
from .date_range import DateRange

class DateGenerator():

    @classmethod
    def today(cls) -> Date:
        obj = Date(datetime.now())

        return obj

    @classmethod
    def yesterday(cls) -> Date:
        obj = cls.today()
        obj.prev()

        return obj

    @classmethod
    def tomorrow(cls) -> Date:
        obj = cls.today()
        obj.next()

        return obj

    @classmethod
    def week(cls, month: int, day: int, year: int) -> DateRange:
        start_dt = Date(month, day, year)

        # set the end date to the end of the week
        end_dt = copy(start_dt)
        end_dt.next(6)

        return DateRange(start_dt, end_dt)

    @classmethod
    def month(cls, month: int, year: int) -> DateRange:
        start_dt = Date(month, 1, year)

        # set the end date to the end of the month
        end_dt = copy(start_dt)
        end_dt.next(28)

        # check if it is still in the month then go one back
        while end_dt._date.month == month:
            end_dt.next()

        end_dt.prev()

        return DateRange(start_dt, end_dt)