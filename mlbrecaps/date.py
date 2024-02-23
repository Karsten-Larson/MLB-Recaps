from functools import total_ordering
from datetime import datetime, timedelta

from typing import Optional

@total_ordering
class Date():
	def __init__(self, date: datetime | str | int, day: Optional[int]=None, year: Optional[int]=None):
		self.setDate(date, day, year)

	def setDate(self, date: datetime | str | int, day: Optional[int]=None, year: Optional[int]=None) -> None:
		match date:
			case str():
				self.date = datetime.strptime(date, "%m/%d/%Y")
			case int():
				self.date: datetime = datetime(year, date, day)
			case _:
				self.date: datetime = date

	def getDate(self) -> datetime:
		return self.date

	def getYear(self) -> int:
		return self.date.year

	# @classmethod
	# def fromDateString(cls, date_string: str) -> 'Date':
	# 	date: Date = cls(datetime.strptime(date_string, "%m/%d/%Y"))

	# 	return date

	# @classmethod
	# def fromDate(cls, month: int, day: int, year: int) -> 'Date':
	# 	date = cls(datetime(year, month, day))

	# 	return date

	def next(self, increment: float=1) -> None:
		self.date += timedelta(days=increment)

	def prev(self, increment: float=1) -> None:
		self.date -= timedelta(days=increment)

	def __copy__(self) -> 'Date':
		month = self.date.month
		day = self.date.day
		year = self.date.year

		return type(self)(datetime(year, month, day))

	def __eq__(self, o: object) -> bool:
		if not isinstance(o, Date):
			return False

		other: Date = o

		return self.date == other.getDate()

	def __lt__(self, o: object) -> bool:
		if not isinstance(o, Date):
			return False

		other: Date = o

		return self.date < other.getDate()

	def __str__(self) -> str:
		return self.date.strftime("%Y-%m-%d")
