from __future__ import annotations

from functools import total_ordering
from datetime import datetime, timedelta

from typing import Optional

@total_ordering
class Date():
	def __init__(self, date: datetime | str | int, day: Optional[int]=None, year: Optional[int]=None):
		self.set_date(date, day, year)

	def set_date(self, date: datetime | str | int, day: Optional[int]=None, year: Optional[int]=None) -> None:
		match date:
			case str():
				self.date = datetime.strptime(date, "%m/%d/%Y")
			case int():
				self.date: datetime = datetime(year, date, day)
			case datetime():
				self.date: datetime = date
			case _:
				raise ValueError("Invalid Date")

	def get_date(self) -> datetime:
		return self.date

	def to_formatted_string(self) -> str:
		return self.date.strftime("%Y-%m-%d")

	def get_year(self) -> int:
		return self.date.year

	def next(self, increment: float=1) -> None:
		self.date += timedelta(days=increment)

	def prev(self, increment: float=1) -> None:
		self.date -= timedelta(days=increment)

	def __copy__(self) -> Date:
		month = self.date.month
		day = self.date.day
		year = self.date.year

		return type(self)(datetime(year, month, day))

	def __eq__(self, o: object) -> bool:
		if not isinstance(o, Date):
			return False

		return self.date == other.get_date()

	def __lt__(self, o: object) -> bool:
		if not isinstance(o, Date):
			return False

		return self.date < other.get_date()

	def __str__(self) -> str:
		return self.date.strftime("%Y-%m-%d")
