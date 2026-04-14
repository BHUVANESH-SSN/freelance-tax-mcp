from __future__ import annotations

from pathlib import Path

from freelance_tax_mcp.memory.models import Invoice
from freelance_tax_mcp.memory.queries import add_invoice
from freelance_tax_mcp.utils.pdf_gen import generate_invoice_pdf
from freelance_tax_mcp.utils.tax_calc import calculate_gst


def generate_invoice_pdf_tool(
	db_path: Path,
	invoice_output_dir: Path,
	user_id: str,
	invoice_number: str,
	freelancer_name: str,
	client_name: str,
	service_description: str,
	amount: float,
	issue_date: str,
	due_date: str,
	gst_rate: float = 18.0,
) -> dict[str, str | float]:
	gst = calculate_gst(amount=amount, gst_rate=gst_rate, intra_state=True)
	invoice_data: dict[str, str | float] = {
		"invoice_number": invoice_number,
		"freelancer_name": freelancer_name,
		"client_name": client_name,
		"service_description": service_description,
		"amount": amount,
		"issue_date": issue_date,
		"due_date": due_date,
		"gst_rate": gst_rate,
		"gst_amount": gst["gst_amount"],
		"invoice_total": gst["invoice_total"],
	}

	output_path = invoice_output_dir / f"{invoice_number}.pdf"
	pdf_path = generate_invoice_pdf(data=invoice_data, output_path=output_path)

	add_invoice(
		db_path=db_path,
		invoice=Invoice(
			user_id=user_id,
			invoice_number=invoice_number,
			client_name=client_name,
			amount=float(gst["invoice_total"]),
			issue_date=issue_date,
			due_date=due_date,
			status="issued",
		),
	)

	return {
		"invoice_number": invoice_number,
		"pdf_path": str(pdf_path),
		"gst_amount": float(gst["gst_amount"]),
		"invoice_total": float(gst["invoice_total"]),
		"status": "generated",
	}

