from typing import Type, Optional
from datetime import datetime, timedelta

class Date():
	
	def setDate(self, month: int, day: int, year: int) -> None:
		self.date: Type["datetime"] = datetime(year, month, day)

	def __init__(self, month: int, day: int, year: int):
		self.setDate(month, day, year)

	def next(self, iter: Optional[int]=1) -> None:
		self.date += timedelta(days=iter)

	def prev(self, iter: Optional[int]=1) -> None:
		self.date -= timedelta(days=iter)

	def __copy__(self):
		month = self.date.month
		day = self.date.day
		year = self.date.year

		return type(self)(month, day, year)

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
