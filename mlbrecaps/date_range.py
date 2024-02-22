from .date import Date

class DateRange():

    def setStartDate(self, start_dt: Date) -> None:
        self.start_dt: Date = start_dt

    def setEndDate(self, end_dt: Date) -> None:
        self.end_dt: Date = end_dt

    def setDates(self, start_dt: Date, end_dt: Date) -> None:
        self.setStartDate(start_dt)
        self.setEndDate(end_dt)

    def __init__(self, start_dt: Date, end_dt: Date):
        self.setDates(start_dt, end_dt)

    def getDates(self) -> tuple[Date, Date]:
        return self.start_dt, self.end_dt
    