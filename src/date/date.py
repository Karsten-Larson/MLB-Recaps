from typing import Type, Optional
from functools import total_ordering
from datetime import datetime, timedelta

@total_ordering
class Date():
	def setDateFromString(self, date_string: str) -> None:
		self.date: Type["datetime"] = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

	def setDate(self, month: int, day: int, year: int) -> None:
		self.date: Type["datetime"] = datetime(year, month, day)

	def __init__(self):
		self.date: Type["datetime"] = None

	def getDate(self) -> Type["datetime"]:
		return self.date

	@classmethod
	def fromDateString(cls, date_string: str):
		date = cls()
		date.setDateFromString(date_string)

		return date

	@classmethod
	def fromDate(cls, month: int, day: int, year: int) -> None:
		date = cls()
		date.setDate(month, day, year)

		return date

	def next(self, iter: Optional[int]=1) -> None:
		self.date += timedelta(days=iter)

	def prev(self, iter: Optional[int]=1) -> None:
		self.date -= timedelta(days=iter)

	def __copy__(self):
		month = self.date.month
		day = self.date.day
		year = self.date.year

		return type(self)(month, day, year)

	def __eq__(self, other):
		return self.date == other.getDate()

	def __lt__(self, other):
		return self.date < other.getDate()

	def __str__(self) -> str:
		return self.date.strftime("%Y-%m-%d")


if __name__ == "__main__":
	from copy import copy

	date = Date.yesterday()

	original_date = copy(date)
	print(f"Yesterday was {date}")

	for i in range(30):
		date.next()
		print(date)

	print(f"Original date: {original_date}")
