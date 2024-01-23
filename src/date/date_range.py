from .date import Date
from types import Type

class DateRange():

    def setStartDate(self, start_dt: Type["Date"]) -> None:
        self.start_dt: Type["Date"] = start_dt

    def setEndDate(self, end_dt: Type["Date"]) -> None:
        self.end_dt: Type["Date"] = end_dt

    def setDates(self, start_dt: Type["Date"], end_dt: Type["Date"]) -> None:
        self.setStartDate(start_dt)
        self.setEndDate(end_dt)

    def __init__(self, start_dt: Type["Date"], end_dt: Type["Date"]):
        self.setDates(start_dt, end_dt)

    def getDates(self) -> tuple[Type["Date"], Type["Date"]]:
        return self.start_dt, self.end_dt
    