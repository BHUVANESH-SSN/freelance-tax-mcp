from __future__ import annotations

from datetime import date

from freelance_tax_mcp.utils.date_helpers import advance_tax_deadlines


def calculate_gst(amount: float, gst_rate: float = 18.0, intra_state: bool = True) -> dict[str, float]:
	taxable_amount = max(amount, 0.0)
	gst_amount = round(taxable_amount * (gst_rate / 100.0), 2)
	total = round(taxable_amount + gst_amount, 2)
	if intra_state:
		cgst = round(gst_amount / 2, 2)
		sgst = round(gst_amount / 2, 2)
		igst = 0.0
	else:
		cgst = 0.0
		sgst = 0.0
		igst = gst_amount
	return {
		"taxable_amount": round(taxable_amount, 2),
		"gst_rate": round(gst_rate, 2),
		"gst_amount": gst_amount,
		"cgst": cgst,
		"sgst": sgst,
		"igst": igst,
		"invoice_total": total,
	}


def _new_regime_tax_2025(income: float) -> float:
	slabs = [
		(400000.0, 0.0),
		(800000.0, 0.05),
		(1200000.0, 0.10),
		(1600000.0, 0.15),
		(2000000.0, 0.20),
		(2400000.0, 0.25),
		(float("inf"), 0.30),
	]
	tax = 0.0
	previous_limit = 0.0
	for limit, rate in slabs:
		if income <= previous_limit:
			break
		slab_income = min(income, limit) - previous_limit
		tax += slab_income * rate
		previous_limit = limit
	return tax


def _old_regime_tax_2025(income: float) -> float:
	slabs = [
		(250000.0, 0.0),
		(500000.0, 0.05),
		(1000000.0, 0.20),
		(float("inf"), 0.30),
	]
	tax = 0.0
	previous_limit = 0.0
	for limit, rate in slabs:
		if income <= previous_limit:
			break
		slab_income = min(income, limit) - previous_limit
		tax += slab_income * rate
		previous_limit = limit
	return tax


def estimate_income_tax(income: float, regime: str = "new") -> dict[str, float | str]:
	taxable_income = max(income, 0.0)
	normalized_regime = regime.lower().strip()
	base_tax = (
		_old_regime_tax_2025(taxable_income)
		if normalized_regime == "old"
		else _new_regime_tax_2025(taxable_income)
	)
	cess = base_tax * 0.04
	total_tax = round(base_tax + cess, 2)
	return {
		"taxable_income": round(taxable_income, 2),
		"regime": normalized_regime,
		"base_tax": round(base_tax, 2),
		"cess_4_percent": round(cess, 2),
		"total_tax": total_tax,
	}


def explain_tax_bracket(annual_income: float, regime: str = "new") -> dict[str, float | str]:
	tax = estimate_income_tax(annual_income, regime)
	effective_rate = 0.0
	if annual_income > 0:
		effective_rate = round((float(tax["total_tax"]) / annual_income) * 100.0, 2)
	tax["effective_rate_percent"] = effective_rate
	return tax


def estimate_advance_tax(
	annual_tax_liability: float,
	paid_so_far: float,
	as_of_date: date | None = None,
) -> dict[str, float | str | list[dict[str, float | str]]]:
	today = as_of_date or date.today()
	fy_start_year = today.year if today.month >= 4 else today.year - 1
	checkpoints = [0.15, 0.45, 0.75, 1.0]
	deadlines = advance_tax_deadlines(fy_start_year)

	installments: list[dict[str, float | str]] = []
	paid = max(paid_so_far, 0.0)
	due_now = 0.0
	next_deadline = "N/A"

	for pct, deadline in zip(checkpoints, deadlines):
		cumulative_due = round(annual_tax_liability * pct, 2)
		required_installment = round(max(cumulative_due - paid, 0.0), 2)
		installments.append(
			{
				"deadline": deadline.isoformat(),
				"required_cumulative_percent": round(pct * 100, 2),
				"required_cumulative_amount": cumulative_due,
				"pay_now_to_stay_compliant": required_installment,
			}
		)
		if deadline >= today and next_deadline == "N/A":
			next_deadline = deadline.isoformat()
			due_now = required_installment

	return {
		"annual_tax_liability": round(annual_tax_liability, 2),
		"paid_so_far": round(paid, 2),
		"next_deadline": next_deadline,
		"due_now": round(due_now, 2),
		"installments": installments,
	}


def check_tds_liability(
	gross_income: float,
	deductible_expenses: float,
	tds_already_deducted: float,
	regime: str = "new",
) -> dict[str, float | str]:
	taxable_income = max(gross_income - deductible_expenses, 0.0)
	tax = estimate_income_tax(taxable_income, regime)
	total_tax = float(tax["total_tax"])
	tds = max(tds_already_deducted, 0.0)
	net_payable = round(total_tax - tds, 2)
	status = "additional_tax_due" if net_payable > 0 else "likely_refund"
	return {
		"gross_income": round(gross_income, 2),
		"deductible_expenses": round(deductible_expenses, 2),
		"taxable_income": round(taxable_income, 2),
		"estimated_total_tax": round(total_tax, 2),
		"tds_already_deducted": round(tds, 2),
		"net_payable": net_payable,
		"status": status,
	}

