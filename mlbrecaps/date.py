from __future__ import annotations

from functools import total_ordering, singledispatchmethod
from datetime import datetime, timedelta

from typing import Optional

@total_ordering
class Date():
	
	def __init__(self, date: datetime | str | int, day: Optional[int]=None, year: Optional[int]=None):
		if day and year:
			self.__set_date(date, day, year)
		else:
			self.__set_date(date)

	@singledispatchmethod
	def __set_date(self, date: datetime | str | int, day: Optional[int]=None, year: Optional[int]=None):
		raise ValueError("Invalid Date")

	@__set_date.register(datetime)
	def _(self, date: datetime):
		self._date = date

	@__set_date.register(str)
	def _(self, date: str):
		self._date = datetime.strptime(date, "%m/%d/%Y")

	@__set_date.register(int)
	def _(self, date: int, day: int, year: int):
		self._date: datetime = datetime(year, date, day)

	@property
	def date(self) -> datetime:
		return self._date

	def to_formatted_string(self) -> str:
		return self._date.strftime("%Y-%m-%d")

	@property
	def year(self) -> int:
		return self._date.year

	@property
	def month(self) -> int:
		return self._date.month

	@property
	def day(self) -> int:
		return self._date.day

	def next(self, increment: float=1) -> None:
		self._date += timedelta(days=increment)

	def prev(self, increment: float=1) -> None:
		self._date -= timedelta(days=increment)

	def copy(self) -> Date:
		month = self._date.month
		day = self._date.day
		year = self._date.year

		return type(self)(datetime(year, month, day))

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Date):
			return False

		return self._date == other.date

	def __lt__(self, other: object) -> bool:
		if not isinstance(other, Date):
			return False

		return self._date < other.date

	def __str__(self) -> str:
		return self._date.strftime("%Y-%m-%d")
