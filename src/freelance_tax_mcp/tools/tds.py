from __future__ import annotations

from freelance_tax_mcp.utils.tax_calc import check_tds_liability


def check_tds_liability_tool(
	gross_income: float,
	deductible_expenses: float,
	tds_already_deducted: float,
	regime: str = "new",
) -> dict[str, float | str]:
	return check_tds_liability(
		gross_income=gross_income,
		deductible_expenses=deductible_expenses,
		tds_already_deducted=tds_already_deducted,
		regime=regime,
	)

