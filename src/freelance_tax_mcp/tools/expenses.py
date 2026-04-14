from __future__ import annotations

from pathlib import Path

from freelance_tax_mcp.memory.models import Transaction
from freelance_tax_mcp.memory.queries import add_transaction


def record_expense_tool(
	db_path: Path,
	user_id: str,
	amount: float,
	expense_date: str,
	category: str,
	notes: str = "",
) -> dict[str, str | float]:
	add_transaction(
		db_path,
		Transaction(
			user_id=user_id,
			txn_type=f"expense:{category}",
			amount=amount,
			txn_date=expense_date,
			notes=notes,
		),
	)
	return {
		"user_id": user_id,
		"amount": round(amount, 2),
		"expense_date": expense_date,
		"category": category,
		"status": "recorded",
	}

