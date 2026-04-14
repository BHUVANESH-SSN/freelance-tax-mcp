from __future__ import annotations

from pathlib import Path

from freelance_tax_mcp.memory.models import Reminder
from freelance_tax_mcp.memory.queries import add_reminder
from freelance_tax_mcp.utils.date_helpers import reminder_title_for_deadline
from freelance_tax_mcp.utils.tax_calc import estimate_advance_tax


def estimate_advance_tax_tool(
	annual_tax_liability: float,
	paid_so_far: float,
	as_of_date: str | None = None,
) -> dict[str, object]:
	if as_of_date:
		year, month, day = [int(p) for p in as_of_date.split("-")]
		from datetime import date

		value = date(year, month, day)
		return estimate_advance_tax(annual_tax_liability, paid_so_far, value)
	return estimate_advance_tax(annual_tax_liability, paid_so_far)


def set_deadline_reminder_tool(
	db_path: Path,
	user_id: str,
	due_date: str,
	kind: str = "advance_tax",
	channel: str = "app",
) -> dict[str, object]:
	title = reminder_title_for_deadline(kind=kind, due_date=due_date)
	reminder = Reminder(user_id=user_id, title=title, due_date=due_date, channel=channel)
	reminder_id = add_reminder(db_path=db_path, reminder=reminder)
	return {
		"reminder_id": reminder_id,
		"user_id": user_id,
		"title": title,
		"due_date": due_date,
		"channel": channel,
		"status": "scheduled",
	}

