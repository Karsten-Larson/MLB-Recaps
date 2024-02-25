from typing import Tuple

from .date import Date

class DateRange():
    def __init__(self, start_dt: Date, end_dt: Date):
        self.set_dates(start_dt, end_dt)

    def set_start_date(self, start_dt: Date) -> None:
        self.start_dt: Date = start_dt

    def set_end_date(self, end_dt: Date) -> None:
        self.end_dt: Date = end_dt

    def set_dates(self, start_dt: Date, end_dt: Date) -> None:
        self.set_start_date(start_dt)
        self.set_end_date(end_dt)

    def get_dates(self) -> tuple[Date, Date]:
        return self.start_dt, self.end_dt
    