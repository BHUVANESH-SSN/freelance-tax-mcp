from freelance_tax_mcp.tools.gst import calculate_gst_tool


def test_calculate_gst_intra_state_split() -> None:
	result = calculate_gst_tool(amount=10000, gst_rate=18, intra_state=True)
	assert result["gst_amount"] == 1800.0
	assert result["cgst"] == 900.0
	assert result["sgst"] == 900.0
	assert result["igst"] == 0.0
	assert result["invoice_total"] == 11800.0


def test_calculate_gst_inter_state_igst() -> None:
	result = calculate_gst_tool(amount=2500, gst_rate=12, intra_state=False)
	assert result["gst_amount"] == 300.0
	assert result["igst"] == 300.0
	assert result["cgst"] == 0.0
	assert result["sgst"] == 0.0

