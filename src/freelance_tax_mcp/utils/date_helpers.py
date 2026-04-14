from __future__ import annotations

from datetime import date, datetime


def parse_date(value: str) -> date:
	return datetime.strptime(value, "%Y-%m-%d").date()


def current_financial_year(today: date | None = None) -> str:
	current = today or date.today()
	if current.month >= 4:
		start = current.year
		end = current.year + 1
	else:
		start = current.year - 1
		end = current.year
	return f"FY {start}-{str(end)[-2:]}"


def advance_tax_deadlines(year: int) -> list[date]:
	return [
		date(year, 6, 15),
		date(year, 9, 15),
		date(year, 12, 15),
		date(year + 1, 3, 15),
	]


def reminder_title_for_deadline(kind: str, due_date: str) -> str:
	return f"{kind} due on {due_date}"

