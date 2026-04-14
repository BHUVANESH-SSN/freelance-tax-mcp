from __future__ import annotations

from freelance_tax_mcp.utils.tax_calc import calculate_gst


def calculate_gst_tool(
	amount: float,
	gst_rate: float = 18.0,
	intra_state: bool = True,
	annual_turnover: float | None = None,
) -> dict[str, float | bool | str]:
	details = calculate_gst(amount=amount, gst_rate=gst_rate, intra_state=intra_state)
	threshold = 2000000.0
	must_register = bool(annual_turnover and annual_turnover >= threshold)
	result: dict[str, float | bool | str] = {
		**details,
		"gst_registration_threshold": threshold,
		"gst_registration_likely_required": must_register,
	}
	if annual_turnover is not None:
		result["annual_turnover"] = round(annual_turnover, 2)
	result["note"] = "GST applicability depends on service category/state rules."
	return result

