from datetime import date

from freelance_tax_mcp.utils.tax_calc import estimate_advance_tax


def test_estimate_advance_tax_generates_four_installments() -> None:
	result = estimate_advance_tax(annual_tax_liability=120000, paid_so_far=0)
	installments = result["installments"]
	assert isinstance(installments, list)
	assert len(installments) == 4
	assert installments[0]["required_cumulative_amount"] == 18000.0
	assert installments[-1]["required_cumulative_amount"] == 120000.0


def test_estimate_advance_tax_due_now_for_july() -> None:
	result = estimate_advance_tax(
		annual_tax_liability=100000,
		paid_so_far=10000,
		as_of_date=date(2026, 7, 1),
	)
	assert result["next_deadline"] == "2026-09-15"
	assert result["due_now"] == 35000.0

